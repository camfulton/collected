import json

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import mtg.models


class Command(BaseCommand):
    FRAMES_MAP = {
        '1993': mtg.models.Printing.OLD,
        '1997': mtg.models.Printing.OLD,
        '2003': mtg.models.Printing.MODERN,
        '2015': mtg.models.Printing.MFIFTEEN,
        'future': mtg.models.Printing.FUTURE,
    }

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print("Updating the database~")

        with open('AllPrintings.json', 'r') as f:
            sets = json.loads(f.read())['data']

            print("Loading up all the sets...")
            self.load_sets(sets)


            print("Loading up all the cards...")
            self.load_cards(sets)

    def load_sets(self, sets, orphan_sets={}, final_run=False):
        for set_code, _set in sets.items():
            obj = {}

            obj['name'] = _set['name']
            obj['release_date'] = _set['releaseDate']
            obj['code'] = _set['code']
            # Can't be null, is populated later when looping through cards
            obj['languages'] = []

            parent_set_code = _set.get('parentCode')

            # Some sets like Zendikar Rising Expeditions have a parent set aka ZNR
            if parent_set_code:
                parent_set = mtg.models.Set.objects.filter(code=parent_set_code).first()
                if not parent_set:
                    # Sometimes we will add a subset before putting the main set into the db
                    # Store them for later and loop over them at the end.
                    orphan_sets[set_code] = _set

                    continue

                # Depopulate the orphan_sets if this is the 2nd time running so we don't recur forever.
                orphan_sets.pop(set_code, None)

                # And add the relation to the model on success.
                obj['parent_set'] = parent_set

            mtg.models.Set.objects.update_or_create(
                name=obj['name'],
                code=obj['code'],
                defaults=obj
            )

        if orphan_sets and not final_run:
            print("Loading up orphan sets...")
            self.load_sets(
                sets,
                orphan_sets=orphan_sets,
                final_run=True
            )

        elif orphan_sets and final_run:
            raise CommandError(
                f'''There were still orphan sets left after the 2nd run.\n
                Here they are: {orphan_sets}
                '''
            )

    def load_cards(self, sets):
        for set_code, _set in sets.items():
            for n, card in enumerate(_set['cards']):
                if n+1 == len(_set['cards']):
                    print(f'Loaded: {n+1}/{len(_set["cards"])} cards from {_set["name"]}', end='\n')
                else:
                    print(f'Loading: {n+1}/{len(_set["cards"])} cards from {_set["name"]}', end='\r')

                card_obj = {}
                printing_obj = {}
                artist_obj = {}

                # Handle the artist
                artist_obj['name'] = card.get('artist', 'MISSING ATTRIBUTION')

                # Handle the card obj
                card_obj['name'] = card['name']
                card_obj['ascii_name'] = card.get('asciiName', card['name'])
                card_obj['color_identity'] = card.get('colorIdentity', [])
                card_obj['colors'] = card.get('colors', [])
                card_obj['cmc'] = card.get('convertedManaCost', '')
                card_obj['manacost'] = card.get('manaCost', '')
                card_obj['reserved'] = card.get('isReserved', False)
                card_obj['keywords'] = card.get('keywords', [])
                card_obj['power'] = card.get('power', '')
                card_obj['toughness'] = card.get('toughness', '')
                card_obj['text'] = card.get('text', '')
                card_obj['types'] = card.get('types', [])
                card_obj['subtypes'] = card.get('subtypes', [])
                card_obj['supertypes'] = card.get('supertypes', [])
                card_obj['typeline'] = card.get('type', '')
                card_obj['side'] = card.get('side', '')

                # Update the set with the languages in the printing
                # The data fidelity here sucks so we try to make it better by combining
                # Bad solution, find a better source
                set_obj = mtg.models.Set.objects.get(code=set_code)
                self.update_set_languages(set_obj, card)

                # Handle the printing obj
                printing_obj['artist'], _ = mtg.models.Artist.objects.update_or_create(
                    name=artist_obj['name'],
                    defaults=artist_obj
                )

                printing_obj['card'], _ = mtg.models.Card.objects.update_or_create(
                    name=card_obj['name'],
                    defaults=card_obj
                )

                printing_obj['set'] = set_obj
                printing_obj['border'] = self.FRAMES_MAP[card['frameVersion']]
                printing_obj['border_color'] = card.get('borderColor', '')
                printing_obj['border_effects'] = card.get('frameEffects', [])
                printing_obj['has_foil'] = card.get('hasFoil')
                printing_obj['has_nonfoil'] = card.get('hasNonFoil')
                printing_obj['full_art'] = card.get('isFullArt', False)
                printing_obj['tcgplayer'] = self.get_tcg_link(card)
                printing_obj['is_original_printing'] = not card.get('isReprint', False)
                printing_obj['flavor_name'] = card.get('flavorName', '')
                printing_obj['flavor_text'] = card.get('flavorText', '')
                printing_obj['is_oversized'] = card.get('isOversized', False)
                printing_obj['is_alternative'] = card.get('isAlternative', False)
                printing_obj['is_promo'] = card.get('isPromo', False)
                printing_obj['is_textless'] = card.get('isTextless', False)
                printing_obj['is_timeshifted'] = card.get('isTimeshifted', False)
                printing_obj['layout'] = card.get('layout', '')
                printing_obj['number'] = card.get('number', '')
                printing_obj['uuid'] = card.get('uuid')
                printing_obj['associated_cards'] = card.get('otherFaceIds', [])
                printing_obj['promo_types'] = card.get('promoTypes', [])
                printing_obj['rarity'] = card.get('rarity', '')
                printing_obj['original_text'] = card.get('originalText', '')
                printing_obj['original_typeline'] = card.get('originalType', '')
                printing_obj['watermark'] = card.get('watermark', '')

                mtg.models.Printing.objects.update_or_create(
                    uuid=printing_obj['uuid'],
                    defaults=printing_obj
                )

    def update_set_languages(self, set_obj, card):
        languages = []

        foreign_data = card.get('foreignData', [])

        for obj in foreign_data:
            if obj['language'] == 'Portuguese (Brazil)':
                obj['language'] = 'Portuguese'

            languages.append(
                mtg.models.Set.LANGUAGES.get(
                    obj['language'],
                    obj['language']
                )
            )

        # Add whatever is missing
        set_obj.languages = list(set().union(set_obj.languages, languages))
        set_obj.save()

    def get_tcg_link(self, card):
        return ''

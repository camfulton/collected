from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField

from mtg.models import Printing


class Collection(models.Model):
    LANGUAGES = [
        'english',
        't_chinese',
        's_chinese',
        'french',
        'german',
        'italian',
        'japanese',
        'korean',
        'portuguese',
        'russian',
        'spanish',
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    english = models.BooleanField(default=True)
    t_chinese = models.BooleanField(default=False)
    s_chinese = models.BooleanField(default=False)
    french = models.BooleanField(default=False)
    german = models.BooleanField(default=False)
    italian = models.BooleanField(default=False)
    japanese = models.BooleanField(default=False)
    korean = models.BooleanField(default=False)
    portuguese = models.BooleanField(default=False)
    russian = models.BooleanField(default=False)
    spanish = models.BooleanField(default=False)

    nonfoil = models.BooleanField(default=True)
    foil = models.BooleanField(default=False)

    border = models.IntegerField(
        choices=Printing.BORDERS,
        blank=True,
        null=True
    )

    cards = models.ManyToManyField(
        'mtg.Card',
        blank=True
    )

    sets = models.ManyToManyField(
        'mtg.Set',
        blank=True
    )

    def __str__(self):
        return f'{self.owner.username}\'s {self.name}'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__length__gt=0), name='non_empty_collection_name'),
        ]

    def generate_cards_collection(self):
        for card in self.cards.all():
            if self.border:
                printings = card.printings.filter(border=self.border)
            else:
                printings = card.printings.all()

            for printing in printings:
                self.create_collection_cards(printing)

    def generate_sets_collection(self):
        for set in self.sets.all():
            printings = set.printings.all()

            for printing in printings:
                self.create_collection_cards(printing)

    def create_collection_cards(self, printing):
        # Cycle through language and foil/nonfoil
        for language in Collection.LANGUAGES:
            if self.collecting_this_language(language, printing):
                if self.foil and printing.has_foil:
                    CollectionCard.objects.create(
                        card=printing.card,
                        printing=printing,
                        uuid=printing.uuid,
                        collected=False,
                        wont_collect=False,
                        language=language,
                        foil=True,
                        collection=self,
                        set_release_date=printing.set.release_date,
                        artist=printing.artist,
                        number=printing.number,
                        set_name=printing.set.name,
                        name=printing.card.name
                    )
                if self.nonfoil and printing.has_nonfoil:
                    CollectionCard.objects.create(
                        card=printing.card,
                        printing=printing,
                        uuid=printing.uuid,
                        collected=False,
                        wont_collect=False,
                        language=language,
                        foil=False,
                        collection=self,
                        set_release_date=printing.set.release_date,
                        artist=printing.artist,
                        number=printing.number,
                        set_name=printing.set.name,
                        name=printing.card.name
                    )

    def collecting_this_language(self, language, printing):
        # If the French box isn't checked, then we are not collecing French
        if not getattr(self, language):
            return False
        # If we are collecting English per ^ and the language is English, then yes
        # We do this check because sets that are English only simply have no languages
        # in the dataset from mtgjson.
        if language == 'english':
            return True
        # If the card doesn't exist in French then we aren't collecting it in French
        # because that would be difficult to do.
        if language not in printing.set.languages:
            return False
        # If you are here it is because the card is in a supported non-english language
        # and there is a printing in this language in this set and you have indicated
        # you would like to collect it.
        return True

    @property
    def table_data(self):
        '''Organize the cards for table display

        Cards Collection:

            {
                'Giant Spider': {                                   <-- sorted on
                    '10E': {
                        'release_date': '2000'                      <-- sorted on
                        'set_name',
                        printings: {
                            'uuid': {
                                number,                             <-- sorted on
                                artist,
                                ccards: {
                                    ('english', 'foil'): {
                                        'id': 12,
                                        'collected': true,
                                        'wont_collect': true,
                                    }
                                }
                            }
                        }
                    }
                },

                'Silklash Spider': {
                    ...
                },

                ...
            }

            Card -
                Edition -
                    Printings -
                Edition
                    Printings
            Card
                Edition
                    Printings
        '''
        data = {}

        if self.cards.exists():
            for ccard in self.collection_cards.all().order_by('card__name', 'printing__set__release_date', 'printing__number'):
                if not data.get(ccard.name):
                    data[ccard.name] = {}

                set_name = ccard.set_name

                if not data[ccard.name].get(set_name):
                    data[ccard.name][set_name] = {}

                    set_data = data[ccard.name][set_name]

                    set_data['release_date'] = ccard.set_release_date
                    set_data['set_name'] = ccard.set_name
                    set_data['printings'] = {}

                set_data = data[ccard.name][set_name]

                if not set_data['printings'].get(ccard.uuid):
                    set_data['printings'][ccard.uuid] = {}

                    uuid_data = set_data['printings'][ccard.uuid]

                    uuid_data['artist'] = ccard.artist
                    uuid_data['number'] = ccard.number
                    uuid_data['ccards'] = {}

                uuid_data = set_data['printings'][ccard.uuid]

                uuid_data[f'{ccard.language}_{ccard.foil}'] = {
                    'id': ccard.id,
                    'collected': ccard.collected,
                    'wont_collect': ccard.wont_collect,
                }

        return data


class CollectionCard(models.Model):
    card = models.ForeignKey(
        'mtg.Card',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    printing = models.ForeignKey(
        'mtg.Printing',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    # Storing this in case I fuck up and delete the card/printing and need to reset them
    uuid = models.UUIDField()

    collected = models.BooleanField(default=False)
    wont_collect = models.BooleanField(default=False)

    language = models.CharField(max_length=50)
    foil = models.BooleanField()

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        related_name='collection_cards'
    )

    name = models.CharField(max_length=250)
    set_name = models.CharField(max_length=100)
    number = models.CharField(max_length=25, default='0')
    artist = models.CharField(max_length=50)
    set_release_date = models.DateField()


    def __str__(self):
        return f'{self.name} | {self.printing.set.release_date} | {self.printing.number}'

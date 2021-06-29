from django.db import models
from django.db.models.functions import Length
from django.contrib.postgres.fields import ArrayField


models.CharField.register_lookup(Length)

class Card(models.Model):
    W = 'W'
    U = 'U'
    B = 'B'
    R = 'R'
    G = 'G'
    C = 'C'

    COLORS = (
        (W, 'White'),
        (U, 'Blue'),
        (B, 'Black'),
        (R, 'Red'),
        (G, 'Green'),
        (C, 'Colorless'),
    )

    name = models.CharField(max_length=250, unique=True)
    ascii_name = models.CharField(max_length=250)
    color_identity = ArrayField(
        models.CharField(max_length=6, choices=COLORS),
        default=list
    )
    colors = ArrayField(
        models.CharField(max_length=6, choices=COLORS),
        default=list
    )
    cmc = models.FloatField(blank=True)
    manacost = models.CharField(max_length=100, blank=True)
    reserved = models.BooleanField(default=False)
    keywords = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    power = models.CharField(max_length=10, blank=True)
    toughness = models.CharField(max_length=10, blank=True)
    text = models.TextField(blank=True)
    types = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    subtypes = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    supertypes = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    typeline = models.CharField(max_length=100, blank=True)
    side = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__length__gt=0), name='non_empty_card_name'),
            models.CheckConstraint(check=models.Q(ascii_name__length__gt=0), name='non_empty_ascii_name'),
        ]


class Printing(models.Model):
    BLACK = 1
    WHITE = 2
    GOLD = 3
    SILVER = 4
    BORDERLESS = 5

    OLD = 1
    MODERN = 2
    FUTURE = 3
    MFIFTEEN = 4

    BONUS = 1
    COMMON = 2
    MYTHIC = 3
    RARE = 4
    SPECIAL = 5
    UNCOMMON = 6

    BORDER_COLORS = (
        (BLACK, 'Black'),
        (WHITE, 'White'),
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BORDERLESS, 'Borderless')
    )

    BORDERS = (
        (OLD, 'Old Border'),
        (MODERN, 'Modern Border'),
        (FUTURE, 'Futureshifted'),
        (MFIFTEEN, 'Magic 2015'),
    )

    RARITIES = (
        (BONUS, 'Bonus'),
        (COMMON, 'Common'),
        (MYTHIC, 'Mythic'),
        (RARE, 'Rare'),
        (SPECIAL, 'Special'),
        (UNCOMMON, 'Uncommon'),
    )

    set = models.ForeignKey('Set', on_delete=models.CASCADE, related_name='printings')
    artist = models.ForeignKey('Artist', on_delete=models.SET_NULL, blank=True, null=True, related_name='printings')
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='printings')
    border = models.IntegerField(choices=BORDERS)
    border_color = models.CharField(max_length=10, choices=BORDER_COLORS)
    border_effects = ArrayField(
        models.CharField(max_length=50, blank=True),
        blank=True,
        default=list
    )
    has_foil = models.BooleanField()
    has_nonfoil = models.BooleanField()
    full_art = models.BooleanField(default=False)
    tcgplayer = models.URLField(blank=True)
    is_original_printing = models.BooleanField()
    flavor_name = models.CharField(max_length=250, blank=True)
    flavor_text = models.TextField(blank=True)
    is_oversized = models.BooleanField()
    is_promo = models.BooleanField()
    is_textless = models.BooleanField()
    is_timeshifted = models.BooleanField()
    is_alternative = models.BooleanField()
    layout = models.CharField(max_length=50)
    number = models.CharField(max_length=25, default='0')
    uuid = models.UUIDField(unique=True)
    associated_cards = ArrayField(
        models.UUIDField(),
        blank=True,
        default=list
    )
    promo_types = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list
    )
    rarity = models.CharField(max_length=8, choices=RARITIES)
    original_text = models.TextField(blank=True)
    original_typeline = models.CharField(max_length=100, blank=True)
    watermark = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.card.name} | {self.set.name}'


    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(border__length__gt=0), name='non_empty_border'),
            models.CheckConstraint(check=models.Q(border_color__length__gt=0), name='non_empty_border_color'),
            models.CheckConstraint(check=models.Q(border_effect__length__gt=0), name='non_empty_border_effect'),
            models.CheckConstraint(check=models.Q(layout__length__gt=0), name='non_empty_layout'),
            models.CheckConstraint(check=models.Q(number__length__gt=0), name='non_empty_number'),
            models.CheckConstraint(check=models.Q(rarity__length__gt=0), name='non_empty_rarity'),
        ]


class Set(models.Model):
    LANGUAGES = {
        'English': 'english',
        'Chinese Traditional': 't_chinese',
        'Chinese Simplified': 's_chinese',
        'French': 'french',
        'German': 'german',
        'Italian': 'italian',
        'Japanese': 'japanese',
        'Korean': 'korean',
        'Portuguese': 'portuguese',
        'Russian': 'russian',
        'Spanish': 'spanish',
    }

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10)
    release_date = models.DateField()
    parent_set = models.ForeignKey(
        'Set',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    languages = ArrayField(
        models.CharField(max_length=25)
    )

    def __str__(self):
        return self.name

    @property
    def has_foil(self):
        return self.printings.filter(has_foil=True).exists()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__length__gt=0), name='non_empty_set_name'),
            models.CheckConstraint(check=models.Q(code__length__gt=0), name='non_empty_code'),
        ]


class Artist(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(name__length__gt=0), name='non_empty_artist_name'),
        ]

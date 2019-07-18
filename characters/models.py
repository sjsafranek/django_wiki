from django.db import models

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
from django.db.models import TextField
from django.db.models import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator


RACES = [
    "Dragonborn",
    "Dwarf",
    "Elf",
    "Gnome",
    "Half-Elf",
    "Half-Orc",
    "Halfling",
    "Human",
    "Tiefling",
    "Changeling",
    "Eladrin",
    "Genasi",
    "Goliath",
    "Minotaur",
    "Shifter",
    "Warforged",
    "Aakakora",
    "Aasimar",
    "Bug Bear",
    "Firbolg",
    "Golbin",
    "Grung",
    "Hobgoblin",
    "Kenku",
    "Kolbold",
    "Lizardfolk",
    "Orc",
    "Tabaxi",
    "Triton",
    "Yuan-Ti Pureblood"
]
RACES.sort()

CLASSES = [
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
    "Artificer"
]
CLASSES.sort()


class Character(models.Model):
    name = models.CharField(max_length=200)
    player_character = BooleanField(default=False)

    gender = models.CharField(
        max_length=8,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    race = models.CharField(
        max_length=20,
        choices=[
            (tag, tag) for tag in RACES
        ]
    )
    subrace = models.CharField(max_length=12)

    class1 = models.CharField(
        max_length=20,
        choices=[
            (tag, tag) for tag in CLASSES
        ]
    )
    subclass1 = models.CharField(max_length=12)

    class2 = models.CharField(
        max_length=20,
        choices=[
            (tag, tag) for tag in CLASSES
        ]
    )
    subclass2 = models.CharField(max_length=12)

    class3 = models.CharField(
        max_length=20,
        choices=[
            (tag, tag) for tag in CLASSES
        ]
    )
    subclass3 = models.CharField(max_length=12)

    class4 = models.CharField(
        max_length=20,
        choices=[
            (tag, tag) for tag in CLASSES
        ]
    )
    subclass4 = models.CharField(max_length=12)

    level = IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    hp = IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5000)]
    )
    ac = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    strength = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    dexterity = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    constitution = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    intelligence = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    wisdom = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    charisma = IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )

    description = TextField()
    biography = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return self.name

    def delete(self):
        self.is_deleted = True
        self.save()

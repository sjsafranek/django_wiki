from django.db import models

from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
from django.db.models import TextField
# from django.db.models import UUIDField


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

class Character(models.Model):
    # id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, editable=False)
    gender = models.CharField(
        max_length=8,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    race = models.CharField(
        max_length=12
        choices=[
            (tag, tag) for tag in RACES
        ]
    )

    subrace = models.CharField(max_length=12)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_deleted = BooleanField(default=False)
    # md5hash

    def __str__(self):
        return self.name

    def deleteFile(self):
        self.is_deleted = True
        self.save()

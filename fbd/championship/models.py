from django.db import models
from django.utils.translation import ugettext_lazy as _


SEX_MALE = 'M'
SEX_FEMALE = 'F'
SEX_NON_BINARY = 'N/B'
SEX_CHOICES = (
    (SEX_MALE, _('Male')),
    (SEX_FEMALE, _('Female')),
    (SEX_NON_BINARY, _('Non-Binary')),
)


class Club(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Player(models.Model):
    club = models.ForeignKey(Club, models.PROTECT, related_name='players')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateTimeField()
    sex = models.CharField(max_length=100, choices=SEX_CHOICES)
    government_id = models.IntegerField(unique=True)
    picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    players = models.ManyToManyField(Player, related_name='tournaments')

    def __str__(self):
        return f'{self.name} on {self.date}'

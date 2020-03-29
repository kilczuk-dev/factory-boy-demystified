from random import randrange

from factory import DjangoModelFactory, Faker, post_generation, lazy_attribute
from factory.fuzzy import FuzzyChoice
from pytz import UTC

from fbd.championship.models import Club, SEX_CHOICES, Player, Tournament


class ClubFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Club


class PlayerFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    dob = Faker('date_time_between', start_date='-40y', end_date='-15y', tzinfo=UTC)
    sex = FuzzyChoice(SEX_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Player

    @lazy_attribute
    def government_id(self):
        # @TODO: improve me
        birth_year = str(self.dob.year)[2:]
        birth_month = str(self.dob.month).zfill(2)
        birth_day = str(self.dob.day).zfill(2)
        counter = str(randrange(1, 10000)).zfill(4)
        return f'{birth_year}{birth_month}{birth_day}{counter}'

    @post_generation
    def tournaments(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tournament in extracted:
                self.tournaments.add(tournament)


class TournamentFactory(DjangoModelFactory):
    name = Faker('sentence', nb_words=2)
    date = Faker('date_time_this_year', after_now=True, tzinfo=UTC)

    class Meta:
        model = Tournament

    @post_generation
    def players(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for player in extracted:
                self.players.add(player)

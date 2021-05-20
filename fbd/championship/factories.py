import os

from django.conf import settings
from django.core.files import File
from django.db.models import Max
from factory import DjangoModelFactory, Faker, post_generation, lazy_attribute_sequence
from factory.fuzzy import FuzzyChoice
from pytz import UTC

from fbd.championship.models import Club, SEX_CHOICES, Player, Tournament, SEX_MALE


class ClubFactory(DjangoModelFactory):
    name = Faker('company')

    class Meta:
        model = Club

    @post_generation
    def players(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for player in extracted:
                player.club = self
                player.save()


class PlayerFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    dob = Faker('date_time_between', start_date='-40y', end_date='-15y', tzinfo=UTC)
    sex = FuzzyChoice(SEX_CHOICES, getter=lambda c: c[0])

    @lazy_attribute_sequence
    def government_id(self, n):
        dob_part = int(self.dob.strftime('%y%m%d')) * 10000

        # lets start at
        # last known government_id for a date + 1 if last known government_id for a date is odd
        # last known government_id for a date + 2 if last known government_id for a date is even
        seq_start = Player.objects.filter(
            government_id__gte=dob_part,
            government_id__lte=dob_part + 10000
        ).aggregate(seq_start=Max('government_id'))['seq_start'] or dob_part
        seq_start += 2 - (seq_start % 2)

        # for male, we need an odd (2n + 1) number, for any other sex - even (2n)
        # n = [0, 1, ..., n]
        government_id = seq_start + 2 * n + (self.sex == SEX_MALE)

        return government_id

    class Meta:
        model = Player

    @post_generation
    def tournaments(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tournament in extracted:
                self.tournaments.add(tournament)

    @post_generation
    def picture(self, create, extracted, **kwargs):
        if extracted:
            self.picture = extracted
        if kwargs:
            assert 'filename' in kwargs, 'You need to pass in the filename'
            location = os.path.join(settings.BASE_DIR, f'fbd/championship/fixtures/{kwargs["filename"]}')
            assert os.path.isfile(location), f'{location} does not exist'
            self.picture = File(open(location, 'rb'))
        if create:
            self.save(update_fields=['picture'])


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

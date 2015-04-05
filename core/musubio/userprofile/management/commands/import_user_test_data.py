import csv, random
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify

from userprofile.models import Profile


FIELD_FIRST_NAME = 0
FIELD_LAST_NAME = 1
FIELD_TEAM_ID = 2
FIELD_POSITION_ID = 3

TEAMS = {
    'SFN': 'San Francisco Giants',
    'LAN': 'Los Angeles Dodgers',
    'COL': 'Colorado Rockies',
    'SDN': 'San Diego Padres',
    'ARI': 'Arizona Diamondbacks',
    'CIN': 'Cincinnati Reds',
    'PIT': 'Pittsburgh Pirates',
    'CHN': 'Chicago Cubs',
    'STL': 'St. Louis Cardinals',
    'MIL': 'Milwaukee Brewers',
    'NYN': 'New York Mets',
    'PHI': 'Philadelphia Phillies',
    'MIA': 'Miami Marlons',
    'ATL': 'Atlanta Braves',
    'WAS': 'Washington Nationals',
    'OAK': 'Oakland Athletics',
    'TEX': 'Texas Rangers',
    'LAA': 'Los Angeles Anges',
    'SEA': 'Seattle Mariners',
    'HOU': 'Houston Astros',
    'CHA': 'Chicago White Sox',
    'CLE': 'Cleveland Indians',
    'DET': 'Detroit Tigers',
    'KCA': 'Kansas City Royals',
    'MIN': 'Minnesota Twins',
    'BAL': 'Baltimore Orioles',
    'NYA': 'New York Yankees',
    'BOS': 'Boston Red Sox',
    'TOR': 'Toronto Blue Jays',
    'TBA': 'Tampa Bay Rays',
}

POSITIONS = {
    'OF': 'Outfielder',
    '1B': 'First Baseman',
    '2B': 'Second Baseman',
    '3B': 'Third Baseman',
    'DH': 'Designated Hitter',
    'C': 'Catcher',
    'SS': 'Short Stop',
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.filter(id__gt=1).delete()

        rows = csv.reader(open('%s/test/data/users.csv' % (settings.MEDIA_ROOT), 'rb'))
        password = make_password('asdfasdf')

        for row in rows:
            # Get random date.
            start_date = date.today().replace(day=1, month=1).toordinal()
            end_date = date.today().toordinal()
            random_date = date.fromordinal(random.randint(start_date, end_date))

            email = '%s.%s@crc-example.com' % (row[FIELD_FIRST_NAME].lower(), row[FIELD_LAST_NAME].lower())
            username = '%s %s' % (row[FIELD_FIRST_NAME].lower(), row[FIELD_LAST_NAME].lower())

            User = get_user_model()
            user = User()
            user.first_name = row[FIELD_FIRST_NAME]
            user.last_name = row[FIELD_LAST_NAME]
            user.email = email
            user.username = slugify(username)
            user.password = password
            user.save()

            user.date_joined = random_date
            user.save()

            title = '%s For The %s' % (POSITIONS[row[FIELD_POSITION_ID]], TEAMS[row[FIELD_TEAM_ID]])

            profile = Profile()
            profile.user = user
            profile.title = title
            profile.save()

            print '[CREATED] User: %s %s' % (user.first_name, user.last_name)
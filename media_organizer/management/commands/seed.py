""" Clear all data and creates objects """
from django.core.management.base import BaseCommand
from media_organizer.models import Movie, Format

import logging

logger = logging.getLogger(__name__)

MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete Movies instances")
    Movie.objects.all().delete()
    logger.info("Delete Formats instances")
    Format.objects.all().delete()



def create_formats():
    """Creates an format object"""
    logger.info("Creating formats")
    format_data = [
        ['Digital Versatile Disc', 'DVD'],
        ['Blu-ray Disc', 'BD'],
        ['Video Home System Videocassette', 'VHS'],
        ['laserdisc', 'LD']
    ]

    for f in format_data:

        format = Format(
            name=f[0],
            abbreviation=f[1]
        )
        format.save()
        logger.info(f'Created {format.__str__}')

def create_movies():
    """Creates an movie object"""
    logger.info("Creating movies")
    movie_data = [
        ['Halloween',['DVD']],
        ['Alien',['BD', 'LD']],
        ['Fargo', ['BD']],
        ['Strangers on a Train', ['VHS', 'LD', 'BD']]
    ]

    for m in movie_data:

        movie = Movie(
            name=m[0],
        )
        movie.save()
        
        for g in m[1]:
            format = Format.objects.get(abbreviation=g)
            movie.formats.add(format)
        
        movie.save()


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return


    create_formats()
    create_movies()
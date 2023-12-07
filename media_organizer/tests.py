from django.test import TestCase
from .models import Movie, Format

class MoviesTestCase(TestCase):

    def setUp(self):
        self.dvd = Format.objects.create(name='Digital Versatile Disc', abbreviation='DVD')
        self.bd = Format.objects.create(name='Blu-ray Disc', abbreviation='BD')

        self.movie_one = Movie.objects.create(name='Fantastic Planet')
        self.movie_two = Movie.objects.create(name='Cat People')

        self.movie_one.formats.add(self.dvd)
        self.movie_one.formats.add(self.bd)
        self.movie_two.formats.add(self.dvd)

    def test_name_is_str(self):
        self.assertIsInstance(self.movie_one.name, str)
        self.assertIsInstance(self.movie_two.name, str)

    def test_str_returns_all_formats(self):
        self.assertIn('DVD', f'{self.movie_one}')
        self.assertIn('BD', f'{self.movie_one}')
        self.assertIn('DVD', f'{self.movie_two}')

    def test_can_have_multiple_formats(self):
        movie = Movie.objects.create(name='Jurassic Park')
        movie.formats.add(self.dvd)
        self.assertEqual(movie.formats.count(), 1)
        movie.formats.add(self.bd)
        self.assertEqual(movie.formats.count(), 2)

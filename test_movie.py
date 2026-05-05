import unittest
import json, os
from main import MovieLibrary

class TestMovieLibrary(unittest.TestCase):
    def setUp(self):
        self.app = MovieLibrary()
        self.app.win.withdraw()
    
    def test_add_valid_movie(self):
        self.app.entry_title.insert(0, "Тестовый фильм")
        self.app.entry_genre.insert(0, "комедия")
        self.app.entry_year.insert(0, "2020")
        self.app.entry_rating.insert(0, "8.5")
        self.app.add_movie()
        self.assertTrue(any(m["title"] == "Тестовый фильм" for m in self.app.movies))
    
    def test_add_empty_title(self):
        initial = len(self.app.movies)
        self.app.entry_title.insert(0, "")
        self.app.entry_genre.insert(0, "драма")
        self.app.entry_year.insert(0, "2020")
        self.app.entry_rating.insert(0, "7")
        self.app.add_movie()
        self.assertEqual(len(self.app.movies), initial)
    
    def test_add_invalid_year(self):
        initial = len(self.app.movies)
        self.app.entry_title.insert(0, "Фильм")
        self.app.entry_genre.insert(0, "боевик")
        self.app.entry_year.insert(0, "год")
        self.app.entry_rating.insert(0, "5")
        self.app.add_movie()
        self.assertEqual(len(self.app.movies), initial)
    
    def test_add_invalid_rating(self):
        initial = len(self.app.movies)
        self.app.entry_title.insert(0, "Фильм")
        self.app.entry_genre.insert(0, "ужасы")
        self.app.entry_year.insert(0, "2019")
        self.app.entry_rating.insert(0, "15")
        self.app.add_movie()
        self.assertEqual(len(self.app.movies), initial)
    
    def test_add_rating_boundary(self):
        self.app.entry_title.insert(0, "Граничный")
        self.app.entry_genre.insert(0, "триллер")
        self.app.entry_year.insert(0, "2021")
        self.app.entry_rating.insert(0, "10")
        self.app.add_movie()
        self.assertTrue(any(m["title"] == "Граничный" for m in self.app.movies))
    
    def test_json_save_load(self):
        test_data = [{"title": "t", "genre": "g", "year": 2000, "rating": 7.5}]
        self.app.save_json("test.json", test_data)
        loaded = self.app.load_json("test.json")
        self.assertEqual(loaded, test_data)
        os.remove("test.json")
    
    def tearDown(self):
        self.app.win.destroy()

if __name__ == "__main__":
    unittest.main()

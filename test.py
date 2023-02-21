import unittest

from esame import ExamException
from esame import CSVTimeSeriesFile
from esame import detect_similar_monthly_variations


class TestExam(unittest.TestCase):

    def test_empty_file(self):
        time_series_file = CSVTimeSeriesFile(name='empty.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(time_series, [])
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, [1949, 1950])

    def test_no_consec_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, [1949, 1952])

    def test_years_not_found(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, [1949, 1800])

    def test_correct_file(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, [1949, 1950]),
                         [False, True, False, True, False, False, False, False, False, False, True])

    def test_missing_entry(self):
        time_series_file = CSVTimeSeriesFile(name='missing.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, [1949, 1950]),
                         [False, False, False, False, False, False, False, False, False, False, False])

    def test_negative_entry(self):
        time_series_file = CSVTimeSeriesFile(name='negative.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, [1949, 1950]),
                         [False, False, False, False, False, False, False, False, False, False, False])

    def test_unordered_data(self):
        time_series_file = CSVTimeSeriesFile(name='unordered.csv')
        self.assertRaises(ExamException, time_series_file.get_data)

    def test_duplicate_data(self):
        time_series_file = CSVTimeSeriesFile(name='duplicate.csv')
        self.assertRaises(ExamException, time_series_file.get_data)

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

    def test_not_Numbers(self):
        time_series_file = CSVTimeSeriesFile(name='notNumber.csv')
        self.assertRaises(ExamException, time_series_file.get_data)

    def test_strange_date_format(self):
        time_series_file = CSVTimeSeriesFile(name='strangeDate.csv')
        self.assertRaises(ExamException, time_series_file.get_data)

    def test_two_str_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, ['1959', '1960']),
                         [False, False, False, False, False, False, False, False, False, False, False])

    def test_two_not_consec_str_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, ['1950', '1960'])

    def test_not_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, ['1950Ciao', '1960'])

    def test_mix_type_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, ['1959', 1960]),
                         [False, False, False, False, False, False, False, False, False, False, False])

    def test_mix_type_not_consec_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, ['1949', 1960])

    def test_negative_years(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, ['-1949', -1960])

    def test_time_series_None(self):
        self.assertRaises(ExamException, detect_similar_monthly_variations, None, [1949, 1950])

    def test_years_None(self):
        time_series_file = CSVTimeSeriesFile(name='data.csv')
        time_series = time_series_file.get_data()
        self.assertRaises(ExamException, detect_similar_monthly_variations, time_series, None)

    def test_time_series_bad_Format_length(self):
        self.assertRaises(ExamException, detect_similar_monthly_variations, [['ciao', 10, 0.09]], [1949, 1950])

    def test_time_series_bad_Format_type(self):
        self.assertRaises(ExamException, detect_similar_monthly_variations, [[1094, '10']], [1949, 1950])

    def test_time_series_bad_Format_date_length(self):
        self.assertRaises(ExamException, detect_similar_monthly_variations,
                          [['1949-1', 10], ['1950-2', 20]], [1949, 1950])

    def test_time_series_bad_Format_pass_type(self):
        self.assertRaises(ExamException, detect_similar_monthly_variations,
                          [['1949-01', 10.01], ['1950-02', 20.1]], [1949, 1950])

    def test_special_char_format_Date(self):
        time_series_file = CSVTimeSeriesFile(name='spaceDate.csv')
        time_series = time_series_file.get_data()
        self.assertEqual(detect_similar_monthly_variations(time_series, [1949, 1950]),
                         [False, True, False, True, False, False, False, False, False, False, True])

import unittest
from datetime import datetime
from kanshi_data import convert_to_wareki

class TestMeishiki(unittest.TestCase):
    def test_wareki_conversion(self):
        """和暦変換のテスト"""
        test_cases = [
            (datetime(2024, 3, 15), '令和6年'),
            (datetime(2019, 5, 1), '令和元年'),
            (datetime(1989, 1, 8), '平成元年'),
            (datetime(1989, 1, 7), '昭和64年'),
            (datetime(1926, 12, 25), '昭和元年'),
            (datetime(1926, 12, 24), '昭和以前')
        ]
        
        for date, expected in test_cases:
            with self.subTest(date=date):
                result = convert_to_wareki(date)
                self.assertEqual(result, expected)

    def test_invalid_date(self):
        """無効な日付のテスト"""
        with self.assertRaises(ValueError):
            convert_to_wareki("invalid_date")

if __name__ == '__main__':
    unittest.main() 
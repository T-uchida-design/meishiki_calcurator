import unittest
from datetime import datetime
import sys
import os

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kanshi_data import get_koyomi_info

class TestKoyomiAPI(unittest.TestCase):
    def test_risshun_2000(self):
        """2000年2月4日の節気を確認"""
        info = get_koyomi_info(2000, 2, 4)
        self.assertEqual(info["sekki"], "立春")

    def test_risshun_2020(self):
        """2020年2月4日の節気を確認"""
        info = get_koyomi_info(2020, 2, 4)
        self.assertEqual(info["sekki"], "立春")

if __name__ == '__main__':
    unittest.main() 
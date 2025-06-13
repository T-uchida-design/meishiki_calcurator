import unittest
from datetime import datetime
import sys
import os

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kanshi_data import calculate_eto, calculate_month_eto, calculate_day_eto

class TestMeishikiCalculation(unittest.TestCase):
    def test_meishiki_2000_01_01(self):
        """2000年1月1日の命式を計算"""
        birth_date = datetime(2000, 1, 1)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2000年1月1日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

    def test_meishiki_2020_02_29(self):
        """2020年2月29日（閏年）の命式を計算"""
        birth_date = datetime(2020, 2, 29)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2020年2月29日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

    def test_meishiki_2024_02_04(self):
        """2024年2月4日（立春）の命式を計算"""
        birth_date = datetime(2024, 2, 4)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2024年2月4日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

    def test_meishiki_2100_01_01(self):
        """2100年1月1日（世紀の変わり目）の命式を計算"""
        birth_date = datetime(2100, 1, 1)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2100年1月1日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

    def test_meishiki_2024_02_03(self):
        """2024年2月3日（立春前日）の命式を計算"""
        birth_date = datetime(2024, 2, 3)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2024年2月3日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

    def test_meishiki_2024_02_05(self):
        """2024年2月5日（立春翌日）の命式を計算"""
        birth_date = datetime(2024, 2, 5)
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        print(f"2024年2月5日の命式: 年柱={eto_nen}, 月柱={eto_getsu}, 日柱={eto_nichi}")

if __name__ == '__main__':
    unittest.main() 
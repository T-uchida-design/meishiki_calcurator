import unittest
from datetime import datetime
import sys
import os

# 親ディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kanshi_data import (
    calculate_eto, calculate_month_eto, calculate_day_eto,
    get_main_zokan, get_days_from_setsuiri_for_shi,
    get_juusei, get_juunisei, get_tenchuu, check_tenchuu_period,
    get_setsuiri_date, convert_to_wareki
)

class TestEdgeCases(unittest.TestCase):
    def test_leap_year(self):
        """閏年のテスト"""
        # 2020年2月29日（閏年）
        birth_date = datetime(2020, 2, 29)
        
        # 干支計算
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        
        # 期待値の検証
        self.assertEqual(eto_nen, '庚子')
        self.assertEqual(eto_getsu, '戊寅')
        self.assertEqual(eto_nichi, '己巳')

    def test_century_change(self):
        """世紀の変わり目のテスト"""
        # 2000年1月1日
        birth_date = datetime(2000, 1, 1)
        
        # 干支計算
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        
        # 期待値の検証
        self.assertEqual(eto_nen, '庚辰')
        self.assertEqual(eto_getsu, '丙子')
        self.assertEqual(eto_nichi, '甲申')

    def test_setsuiri_boundary(self):
        """節入りの前後のテスト"""
        # 2024年2月4日（立春）
        birth_date = datetime(2024, 2, 4)
        
        # 干支計算
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)
        
        # 期待値の検証
        self.assertEqual(eto_nen, '甲辰')
        self.assertEqual(eto_getsu, '丙寅')
        self.assertEqual(eto_nichi, '丙午')

    def test_main_zokan_calculation(self):
        """主蔵干計算のエッジケース"""
        # 節入り前後の主蔵干計算
        birth_date = datetime(2024, 2, 3)  # 立春前日
        
        # 地支と日数から主蔵干を計算
        days = get_days_from_setsuiri_for_shi(birth_date, '寅')
        main_zokan = get_main_zokan('寅', days)
        
        # 期待値の検証
        self.assertEqual(main_zokan, '丙')

    def test_tenchuu_calculation(self):
        """天中殺計算のエッジケース"""
        # 天中殺が重なるケース
        birth_date = datetime(2024, 2, 4)
        
        # 天中殺計算
        tenchuu = get_tenchuu('辰', '寅')
        tenchuu_periods = check_tenchuu_period(birth_date, tenchuu)
        
        # 期待値の検証
        self.assertIsNotNone(tenchuu)
        self.assertTrue(len(tenchuu_periods) > 0)

    def test_setsuiri_and_zokan_for_19800123(self):
        from datetime import datetime as dt
        birth_date = dt(1980, 1, 23)
        # 1. 節入り日
        setsuiri = get_setsuiri_date(birth_date)
        print(f"1980年1月23日の節入り日: {setsuiri}")
        # 2. 丑の主蔵干
        days = get_days_from_setsuiri_for_shi(birth_date, '丑')
        print(f"丑の節入りからの日数: {days}")
        main_zokan = get_main_zokan('丑', days)
        print(f"丑の主蔵干: {main_zokan}")
        # 3. 未の主蔵干
        days_uma = get_days_from_setsuiri_for_shi(birth_date, '未')
        main_zokan_uma = get_main_zokan('未', days_uma)
        print(f"未の主蔵干: {main_zokan_uma}")

    def test_setsuiri_date_and_days_1980_01_23(self):
        from datetime import datetime as dt
        from meishiki_calculator.kanshi_data import get_setsuiri_date, get_days_from_setsuiri_for_shi
        birth_date = dt(1980, 1, 23)
        setsuiri = get_setsuiri_date(birth_date)
        print(f"1980年1月23日の節入り日: {setsuiri}")
        days_from_setsuiri = get_days_from_setsuiri_for_shi(birth_date, '丑')
        print(f"1980年1月23日（丑）の節入りからの日数: {days_from_setsuiri}")

    def test_19800123_setsuiri_and_zokan(self):
        from datetime import date
        from meishiki_calculator.kanshi_data import get_setsuiri_date, get_days_from_setsuiri_for_shi, get_main_zokan
        birth_date = date(1980, 1, 23)
        setsuiri = get_setsuiri_date(birth_date)
        print(f"1980年1月23日の節入り日: {setsuiri}")
        for shi in ['丑', '未']:
            days = get_days_from_setsuiri_for_shi(birth_date, shi)
            print(f"支={shi} の節入りからの日数: {days}")
            zokan = get_main_zokan(shi, days)
            print(f"支={shi} の主蔵干: {zokan}")

    def test_1980_01_23_setsuiri_and_days(self):
        import datetime
        from meishiki_calculator.kanshi_data import get_setsuiri_date, get_days_from_setsuiri_for_shi
        birth_date = datetime.date(1980, 1, 23)
        setsuiri = get_setsuiri_date(birth_date)
        print(f"1980年1月23日の節入り日: {setsuiri}")
        days_from_setsuiri = get_days_from_setsuiri_for_shi(birth_date, '丑')
        print(f"1980年1月23日（丑）の節入りからの日数: {days_from_setsuiri}")

if __name__ == '__main__':
    unittest.main() 
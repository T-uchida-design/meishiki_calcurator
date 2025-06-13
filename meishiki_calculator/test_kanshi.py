from datetime import datetime
from meishiki_calculator.kanshi_data import (
    calculate_eto, calculate_month_eto, calculate_day_eto, get_zokan,
    get_juusei, get_juunisei, get_days_from_setsuiri, get_main_zokan, get_days_from_setsuiri_for_shi,
    get_koyomi_info, JUUSEI_TABLE, JUUNISEI_TABLE, check_tenchuu_period, get_setsuiri_date
)

# 太郎さんの正しい命式（1988年11月1日）
print("=== 太郎さんの正解（画像より）===")
print("日柱: 庚申 (主蔵干: 庚)")
print("月柱: 戊戌 (主蔵干: 辛)")  
print("年柱: 戊辰 (主蔵干: 乙)")

print("\n人体図:")
print("        龍高    天印")
print("貴象    龍高    龍高")
print("天極    鳳閣    天堂")
print("龍高    石門    司禄")  
print("鳳閣    牽牛    調舒")

# 太郎さんの干支と主蔵干
taro_nichi_kan, taro_nichi_shi = '庚', '申'
taro_getsu_kan, taro_getsu_shi = '戊', '戌'
taro_nen_kan, taro_nen_shi = '戊', '辰'

taro_main_zokan_nichi = '庚'  # 申の主蔵干
taro_main_zokan_getsu = '辛'  # 戌の主蔵干
taro_main_zokan_nen = '乙'    # 辰の主蔵干

print(f"\n=== 太郎さんの命式で星を逆算 ===")
print("利用可能な天干:", [taro_nichi_kan, taro_getsu_kan, taro_nen_kan])
print("利用可能な主蔵干:", [taro_main_zokan_nichi, taro_main_zokan_getsu, taro_main_zokan_nen])
print("利用可能な地支:", [taro_nichi_shi, taro_getsu_shi, taro_nen_shi])

# 人体図にある星を分類
juusei_stars = ['龍高', '貴象', '鳳閣', '石門', '司禄', '牽牛', '調舒']  # 十大主星系
juunisei_stars = ['天印', '天極', '天堂']  # 十二大従星系

print(f"\n=== 十大主星系の星 ===")
kans = [taro_nichi_kan, taro_getsu_kan, taro_nen_kan]
zokans = [taro_main_zokan_nichi, taro_main_zokan_getsu, taro_main_zokan_nen]

for star in juusei_stars:
    print(f"{star}を作る組み合わせ:")
    found = False
    for kan in kans:
        for zokan in zokans:
            result = get_juusei(kan, zokan)
            if result == star:
                print(f"  {kan} × {zokan} = {result}")
                found = True
    if not found:
        print(f"  見つかりません")

print(f"\n=== 十二大従星系の星 ===")
shis = [taro_nichi_shi, taro_getsu_shi, taro_nen_shi]

for star in juunisei_stars:
    print(f"{star}を作る組み合わせ:")
    found = False
    for kan in kans:
        for shi in shis:
            result = get_juunisei(kan, shi)
            if result == star:
                print(f"  {kan} × {shi} = {result}")
                found = True
    if not found:
        print(f"  見つかりません")

# さらに詳しく：全ての組み合わせを表示
print(f"\n=== 全ての組み合わせの結果 ===")
print("十大主星（天干×主蔵干）:")
for kan in kans:
    for zokan in zokans:
        result = get_juusei(kan, zokan)
        print(f"  {kan} × {zokan} = {result}")

print("\n十二大従星（天干×地支）:")
for kan in kans:
    for shi in shis:
        result = get_juunisei(kan, shi)
        print(f"  {kan} × {shi} = {result}")

# 1982年3月12日の命式
birth_date = datetime(1982, 3, 12)

eto_nen = calculate_eto(birth_date)
eto_getsu = calculate_month_eto(birth_date)
eto_nichi = calculate_day_eto(birth_date)

nen_kan, nen_shi = eto_nen[0], eto_nen[1]
getsu_kan, getsu_shi = eto_getsu[0], eto_getsu[1]
nichi_kan, nichi_shi = eto_nichi[0], eto_nichi[1]

try:
    days_nen = get_days_from_setsuiri_for_shi(birth_date, nen_shi)
except:
    days_nen = 0

try:
    days_getsu = get_days_from_setsuiri_for_shi(birth_date, getsu_shi)
except:
    days_getsu = 0

try:
    days_nichi = get_days_from_setsuiri_for_shi(birth_date, nichi_shi)
except:
    days_nichi = 0

main_zokan_nen = get_main_zokan(nen_shi, days_nen)
main_zokan_getsu = get_main_zokan(getsu_shi, days_getsu)
main_zokan_nichi = get_main_zokan(nichi_shi, days_nichi)

# 天中殺計算
tenchuu = get_tenchuu(nen_shi, getsu_shi)
tenchuu_periods = check_tenchuu_period(birth_date, tenchuu)

# 陰占
print("=== 1982年3月12日の命式 ===")
print("陰占（干支・蔵干・主蔵干）")
print("日\t月\t年")
print(f"{nichi_kan}\t{getsu_kan}\t{nen_kan}")
print(f"{nichi_shi}\t{getsu_shi}\t{nen_shi}")
print(f"{main_zokan_nichi}\t{main_zokan_getsu}\t{main_zokan_nen}")

# 陽占（正しい算命学の方法）
print(f"\n陽占（人体図：日干{nichi_kan}を中心とした計算）")

# 配置：
# 日月年
# 甲癸壬
# 午卯戌
# 丁乙辛
#
#   ①(壬) a(戌)
# ⑤(丁) ③(乙) ④(辛)  
# c(午) ②(癸) b(卯)

# 十大主星：日干から蔵干を見る
star_1 = get_juusei(nichi_kan, nen_kan)        # 甲から壬を見る
star_2 = get_juusei(nichi_kan, getsu_kan)      # 甲から癸を見る  
star_3 = get_juusei(nichi_kan, main_zokan_getsu)  # 甲から乙を見る
star_4 = get_juusei(nichi_kan, main_zokan_nen)    # 甲から辛を見る
star_5 = get_juusei(nichi_kan, main_zokan_nichi)  # 甲から丁を見る

# 十二大従星：日干から地支を見る
star_a = get_juunisei(nichi_kan, nen_shi)      # 甲から戌を見る
star_b = get_juunisei(nichi_kan, getsu_shi)    # 甲から卯を見る
star_c = get_juunisei(nichi_kan, nichi_shi)    # 甲から午を見る

# 人体図表示
print(f"  {star_1}\t{star_a}")
print(f"{star_5}\t{star_3}\t{star_4}")
print(f"{star_c}\t{star_2}\t{star_b}")

print(f"\n詳細計算:")
print(f"①: {star_1} (日干{nichi_kan}×年干{nen_kan})")
print(f"②: {star_2} (日干{nichi_kan}×月干{getsu_kan})")
print(f"③: {star_3} (日干{nichi_kan}×月支主蔵干{main_zokan_getsu})")
print(f"④: {star_4} (日干{nichi_kan}×年支主蔵干{main_zokan_nen})")
print(f"⑤: {star_5} (日干{nichi_kan}×日支主蔵干{main_zokan_nichi})")
print(f"a: {star_a} (日干{nichi_kan}×年支{nen_shi})")
print(f"b: {star_b} (日干{nichi_kan}×月支{getsu_shi})")
print(f"c: {star_c} (日干{nichi_kan}×日支{nichi_shi})")

# 天中殺
print(f"\n天中殺:")
print(f"運命天中殺: {tenchuu}")
print(f"天中殺期間: {', '.join(tenchuu_periods)}")

# 検証：例題（丙壬庚/申午午/戊己己）
print(f"\n=== 例題検証（修正版） ===")
print("例題: 丙壬庚/申午午/戊己己")

example_nichi_kan = '丙'
example_getsu_kan = '壬'
example_nen_kan = '庚'
example_nichi_shi = '申'
example_getsu_shi = '午'
example_nen_shi = '午'
example_main_zokan_nichi = '戊'
example_main_zokan_getsu = '己'
example_main_zokan_nen = '己'

ex_star_1 = get_juusei(example_nichi_kan, example_nen_kan)        # 丙から庚
ex_star_2 = get_juusei(example_nichi_kan, example_getsu_kan)      # 丙から壬
ex_star_3 = get_juusei(example_nichi_kan, example_main_zokan_getsu)  # 丙から己
ex_star_4 = get_juusei(example_nichi_kan, example_main_zokan_nen)    # 丙から己
ex_star_5 = get_juusei(example_nichi_kan, example_main_zokan_nichi)  # 丙から戊

ex_star_a = get_juunisei(example_nichi_kan, example_nen_shi)      # 丙から午
ex_star_b = get_juunisei(example_nichi_kan, example_getsu_shi)    # 丙から午
ex_star_c = get_juunisei(example_nichi_kan, example_nichi_shi)    # 丙から申

print(f"計算結果:")
print(f"  {ex_star_1}\t{ex_star_a}")
print(f"{ex_star_5}\t{ex_star_3}\t{ex_star_4}")
print(f"{ex_star_c}\t{ex_star_2}\t{ex_star_b}")

print(f"\n正解:")
print(f"  禄存星\t天将星")
print(f"鳳閣星\t調舒星\t調舒星")
print(f"天胡星\t車騎星\t天将星")

# 検証確認
print(f"\n修正確認:")
print(f"丙×午 = {get_juunisei('丙', '午')} (正解: 天将星)")
print(f"丙×申 = {get_juunisei('丙', '申')} (正解: 天胡星)")

# 太郎さん（1988年11月11日）の天中殺も確認
taro_tenchuu = get_tenchuu('辰', '戌')
print(f"\n太郎さん（1988年11月11日）の天中殺:")
print(f"運命天中殺: {taro_tenchuu}")

# test_debug_19800123だけ有効

def test_debug_19800123():
    from datetime import datetime as dt
    birth_date = dt(1980, 1, 23)
    print('生年月日:', birth_date)
    setsuiri = get_setsuiri_date(birth_date)
    print('節入り日:', setsuiri)
    days_from_setsuiri = (birth_date - setsuiri).days
    print('節入りからの日数:', days_from_setsuiri)
    for shi in ['丑', '未']:
        days = get_days_from_setsuiri_for_shi(birth_date, shi)
        print(f'{shi} の節入りからの日数:', days)
        main_zokan = get_main_zokan(shi, days)
        print(f'{shi} の主蔵干:', main_zokan)

# 直接実行用
if __name__ == "__main__":
    test_debug_19800123() 
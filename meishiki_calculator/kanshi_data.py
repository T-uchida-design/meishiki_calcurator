import requests
import pandas as pd
import datetime
from datetime import timedelta

JIKKAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
JUNISHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 蔵干テーブル
ZOKAN_TABLE = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}

# 蔵干日数表（全地支・21日分サンプル）
ZOKAN_DAY_TABLE = {
    '子': ['癸'] * 21,
    '丑': ['己'] * 10 + ['癸'] * 10 + ['辛'],
    '寅': ['甲'] * 7 + ['丙'] * 7 + ['戊'] * 7,
    '卯': ['乙'] * 21,
    '辰': ['戊'] * 6 + ['乙'] * 6 + ['癸'] * 6 + ['戊'] * 3,
    '巳': ['丙'] * 6 + ['戊'] * 6 + ['庚'] * 6 + ['丙'] * 3,
    '午': ['丁'] * 10 + ['己'] * 10 + ['丁'],
    '未': ['己'] * 7 + ['丁'] * 7 + ['乙'] * 7,
    '申': ['庚'] * 6 + ['壬'] * 6 + ['戊'] * 6 + ['庚'] * 3,
    '酉': ['辛'] * 21,
    '戌': ['戊'] * 6 + ['辛'] * 6 + ['丁'] * 6 + ['戊'] * 3,
    '亥': ['壬'] * 10 + ['甲'] * 10 + ['壬'],
}

def get_zokan(jishi):
    """地支から蔵干リストを取得"""
    return ZOKAN_TABLE.get(jishi, [])

def get_main_zokan(shi, days_from_setsuiri):
    """
    支（地支）と節入りからの日数から主蔵干を返す（ユーザー指定ルール）
    """
    if shi == '子':
        return '癸'
    elif shi == '丑':
        if days_from_setsuiri <= 8:
            return '癸'
        elif 9 <= days_from_setsuiri <= 11:
            return '辛'
        else:
            return '己'
    elif shi == '寅':
        if days_from_setsuiri <= 6:
            return '戊'
        elif 7 <= days_from_setsuiri <= 13:
            return '丙'
        else:
            return '甲'
    elif shi == '卯':
        return '乙'
    elif shi == '辰':
        if days_from_setsuiri <= 8:
            return '乙'
        elif 9 <= days_from_setsuiri <= 11:
            return '癸'
        else:
            return '戊'
    elif shi == '巳':
        if days_from_setsuiri <= 4:
            return '戊'
        elif 5 <= days_from_setsuiri <= 13:
            return '庚'
        else:
            return '丙'
    elif shi == '午':
        if days_from_setsuiri <= 18:
            return '己'
        else:
            return '丁'
    elif shi == '未':
        if days_from_setsuiri <= 8:
            return '丁'
        elif 9 <= days_from_setsuiri <= 11:
            return '乙'
        else:
            return '己'
    elif shi == '申':
        if days_from_setsuiri <= 9:
            return '戊'
        elif 10 <= days_from_setsuiri <= 12:
            return '壬'
        else:
            return '庚'
    elif shi == '酉':
        return '辛'
    elif shi == '戌':
        if days_from_setsuiri <= 8:
            return '辛'
        elif 9 <= days_from_setsuiri <= 11:
            return '丁'
        else:
            return '戊'
    elif shi == '亥':
        if days_from_setsuiri <= 11:
            return '甲'
        else:
            return '壬'
    return ''

KOYOMI_API = "https://koyomi.zingsystem.com/api/"

# APIから暦情報を取得
def get_koyomi_info(year, month, day):
    url = f"{KOYOMI_API}?mode=d&cnt=1&targetyyyy={year}&targetmm={month}&targetdd={day}"
    response = requests.get(url)
    data = response.json()
    return data["datelist"][f"{year:04d}-{month:02d}-{day:02d}"]

# 立春の日付を取得
def get_risshun_date(year):
    for day in range(1, 15):
        info = get_koyomi_info(year, 2, day)
        if info["sekki"] == "立春":
            return datetime.datetime(year, 2, day)
    raise ValueError("立春が見つかりません")

# 年柱（六十干支表ロジック）
def calculate_eto(date):
    risshun = get_risshun_date(date.year)
    if date < risshun:
        year = date.year - 1
    else:
        year = date.year
    cycle = (year - 4) % 60
    jikkan_index = cycle % 10
    junishi_index = cycle % 12
    return JIKKAN[jikkan_index] + JUNISHI[junishi_index]

# 直近の節入り日を取得
def get_setsuiri_date(date):
    sekki_list = ["立春", "啓蟄", "清明", "立夏", "芒種", "小暑", "立秋", "白露", "寒露", "立冬", "大雪", "小寒"]
    last_setsuiri = None
    # 前月と当月を探索
    for m in [date.month - 1 if date.month > 1 else 12, date.month]:
        y = date.year if not (m == 12 and date.month == 1) else date.year - 1
        for day in range(1, 16):
            try:
                info = get_koyomi_info(y, m, day)
                if info["sekki"] in sekki_list:
                    setsuiri = datetime.datetime(y, m, day)
                    if setsuiri <= date:
                        if (last_setsuiri is None) or (setsuiri > last_setsuiri):
                            last_setsuiri = setsuiri
            except:
                continue
    if last_setsuiri is None:
        raise ValueError("節入り日が見つかりません")
    return last_setsuiri

# 月柱（六十干支表ロジック）
def calculate_month_eto(date):
    setsuiri = get_setsuiri_date(date)
    # 年干取得（年柱と同じロジック）
    risshun = get_risshun_date(setsuiri.year)
    if setsuiri < risshun:
        year = setsuiri.year - 1
    else:
        year = setsuiri.year
    year_kan_index = (year - 4) % 10
    year_kan = JIKKAN[year_kan_index]
    # 節月（寅月=1, 卯月=2, ... 丑月=12）
    setsuiri_month = ((setsuiri.month + 10) % 12) + 1
    # 月干スタート位置
    month_start = {
        '甲': 2, '己': 2,  # 丙
        '乙': 4, '庚': 4,  # 戊
        '丙': 6, '辛': 6,  # 庚
        '丁': 8, '壬': 8,  # 壬
        '戊': 0, '癸': 0   # 甲
    }[year_kan]
    jikkan_index = (month_start + setsuiri_month - 1) % 10
    junishi_index = (setsuiri_month + 1) % 12  # 寅からスタート
    return JIKKAN[jikkan_index] + JUNISHI[junishi_index]

# 日柱（APIのその日）
def calculate_day_eto(date):
    info = get_koyomi_info(date.year, date.month, date.day)
    return info["zyusi"] + info["zyunisi"]

def convert_to_wareki(y_m_d):
    """西暦の年月日を和暦の年に変換する"""
    if WAREKI_START['令和'] <= y_m_d:
        year = y_m_d.year - WAREKI_START['令和'].year + 1
        era = '令和'
    elif WAREKI_START['平成'] <= y_m_d:
        year = y_m_d.year - WAREKI_START['平成'].year + 1
        era = '平成'
    elif WAREKI_START['昭和'] <= y_m_d:
        year = y_m_d.year - WAREKI_START['昭和'].year + 1
        era = '昭和'
    else:
        return '昭和以前'
    
    return f"{era}{'元' if year == 1 else year}年"

def get_setsuiri_month_2025(date):
    for month in range(2, 13):
        if date < SETSUIRI_2025[month]:
            return month - 1
    return 12

def get_ritsushun_year(date):
    """立春を考慮した年を計算する"""
    # 2024年の立春を基準に計算
    base_year = 2024
    year_diff = date.year - base_year
    ritsushun = datetime.datetime(SETSUIRI_2025[2].year + year_diff, SETSUIRI_2025[2].month, SETSUIRI_2025[2].day)
    
    # 立春前なら前年
    if date < ritsushun:
        return date.year - 1
    return date.year

def calculate_hour_eto(date, hour):
    """日付と時刻から時の干支を計算する"""
    # 日の干支を基準に計算
    day_cycle = (date - datetime.datetime(1900, 1, 1)).days % 60
    # 時刻は2時間ごとに干支が変わる
    hour_index = hour // 2
    jikkan_index = (day_cycle * 2 + hour_index) % 10
    junishi_index = hour_index % 12
    
    return JIKKAN[jikkan_index] + JUNISHI[junishi_index]

# 十大主星表（日干×蔵干で十大主星を決定）
JUUSEI_TABLE = {
    '甲': {
        '甲': '貫索星', '乙': '石門星', '丙': '鳳閣星', '丁': '調舒星', '戊': '禄存星',
        '己': '司禄星', '庚': '車騎星', '辛': '牽牛星', '壬': '龍高星', '癸': '玉堂星'
    },
    '乙': {
        '甲': '石門星', '乙': '貫索星', '丙': '調舒星', '丁': '鳳閣星', '戊': '司禄星',
        '己': '禄存星', '庚': '牽牛星', '辛': '車騎星', '壬': '玉堂星', '癸': '龍高星'
    },
    '丙': {
        '甲': '龍高星', '乙': '玉堂星', '丙': '貫索星', '丁': '石門星', '戊': '鳳閣星',
        '己': '調舒星', '庚': '禄存星', '辛': '司禄星', '壬': '車騎星', '癸': '牽牛星'
    },
    '丁': {
        '甲': '玉堂星', '乙': '龍高星', '丙': '石門星', '丁': '貫索星', '戊': '調舒星',
        '己': '鳳閣星', '庚': '司禄星', '辛': '禄存星', '壬': '牽牛星', '癸': '車騎星'
    },
    '戊': {
        '甲': '車騎星', '乙': '牽牛星', '丙': '龍高星', '丁': '玉堂星', '戊': '貫索星',
        '己': '石門星', '庚': '鳳閣星', '辛': '調舒星', '壬': '禄存星', '癸': '司禄星'
    },
    '己': {
        '甲': '牽牛星', '乙': '車騎星', '丙': '玉堂星', '丁': '龍高星', '戊': '石門星',
        '己': '貫索星', '庚': '調舒星', '辛': '鳳閣星', '壬': '司禄星', '癸': '禄存星'
    },
    '庚': {
        '甲': '禄存星', '乙': '司禄星', '丙': '車騎星', '丁': '牽牛星', '戊': '龍高星',
        '己': '玉堂星', '庚': '貫索星', '辛': '石門星', '壬': '鳳閣星', '癸': '調舒星'
    },
    '辛': {
        '甲': '司禄星', '乙': '禄存星', '丙': '牽牛星', '丁': '車騎星', '戊': '玉堂星',
        '己': '龍高星', '庚': '石門星', '辛': '貫索星', '壬': '調舒星', '癸': '鳳閣星'
    },
    '壬': {
        '甲': '鳳閣星', '乙': '調舒星', '丙': '禄存星', '丁': '司禄星', '戊': '車騎星',
        '己': '牽牛星', '庚': '龍高星', '辛': '玉堂星', '壬': '貫索星', '癸': '石門星'
    },
    '癸': {
        '甲': '調舒星', '乙': '鳳閣星', '丙': '司禄星', '丁': '禄存星', '戊': '牽牛星',
        '己': '車騎星', '庚': '玉堂星', '辛': '龍高星', '壬': '石門星', '癸': '貫索星'
    }
}

# 十二大従星表（日干×年支・月支・日支の各蔵干で決定）
# 算命学Stockの正確な情報に基づいて修正　　 # 天報星　天印星　天貴星　天恍星　天南星　天禄星　天将星　天堂星　天胡星　天極星　天庫星　天馳星
JUUNISEI_TABLE = {
    '甲': {'子': '天恍星', '丑': '天南星', '寅': '天禄星', '卯': '天将星', '辰': '天堂星', '巳': '天胡星', '午': '天極星', '未': '天庫星', '申': '天馳星', '酉': '天報星', '戌': '天印星', '亥': '天貴星'},
    '乙': {'子': '天胡星', '丑': '天堂星', '寅': '天将星', '卯': '天禄星', '辰': '天南星', '巳': '天恍星', '午': '天貴星', '未': '天印星', '申': '天報星', '酉': '天馳星', '戌': '天庫星', '亥': '天極星'},
    '丙': {'子': '天報星', '丑': '天印星', '寅': '天貴星', '卯': '天恍星', '辰': '天南星', '巳': '天禄星', '午': '天将星', '未': '天堂星', '申': '天胡星', '酉': '天極星', '戌': '天庫星', '亥': '天馳星'},
    '丁': {'子': '天馳星', '丑': '天庫星', '寅': '天極星', '卯': '天胡星', '辰': '天堂星', '巳': '天将星', '午': '天禄星', '未': '天南星', '申': '天恍星', '酉': '天貴星', '戌': '天印星', '亥': '天報星'},
    '戊': {'子': '天報星', '丑': '天印星', '寅': '天貴星', '卯': '天恍星', '辰': '天南星', '巳': '天禄星', '午': '天将星', '未': '天堂星', '申': '天胡星', '酉': '天極星', '戌': '天庫星', '亥': '天馳星'},
    '己': {'子': '天馳星', '丑': '天庫星', '寅': '天極星', '卯': '天胡星', '辰': '天堂星', '巳': '天将星', '午': '天禄星', '未': '天南星', '申': '天恍星', '酉': '天貴星', '戌': '天印星', '亥': '天報星'},
    '庚': {'子': '天極星', '丑': '天馳星', '寅': '天報星', '卯': '天印星', '辰': '天貴星', '巳': '天恍星', '午': '天南星', '未': '天禄星', '申': '天将星', '酉': '天堂星', '戌': '天胡星', '亥': '天極星'},
    '辛': {'子': '天貴星', '丑': '天印星', '寅': '天報星', '卯': '天馳星', '辰': '天庫星', '巳': '天極星', '午': '天胡星', '未': '天堂星', '申': '天将星', '酉': '天禄星', '戌': '天南星', '亥': '天恍星'},
    '壬': {'子': '天将星', '丑': '天堂星', '寅': '天胡星', '卯': '天極星', '辰': '天庫星', '巳': '天馳星', '午': '天報星', '未': '天印星', '申': '天貴星', '酉': '天恍星', '戌': '天南星', '亥': '天禄星'},
    '癸': {'子': '天禄星', '丑': '天南星', '寅': '天恍星', '卯': '天貴星', '辰': '天印星', '巳': '天報星', '午': '天馳星', '未': '天庫星', '申': '天極星', '酉': '天胡星', '戌': '天堂星', '亥': '天将星'}
}

def get_juusei(nichi_kan, zokan):
    """十大主星を取得（日干×蔵干）"""
    return JUUSEI_TABLE.get(nichi_kan, {}).get(zokan, "")

def get_juunisei(kan, shi):
    """十二大従星を取得"""
    return JUUNISEI_TABLE.get(kan, {}).get(shi, "")

def get_days_from_setsuiri(birth_date):
    setsuiri = get_setsuiri_date(birth_date)
    return (birth_date - setsuiri).days 

def get_days_from_setsuiri_for_shi(birth_date, shi):
    """
    指定した支（地支）の節入り日からbirth_dateまでの日数を返す。
    - shi: '子'～'亥'
    - birth_dateの月の支と一致する場合は、その月の節入り日を参照
    """
    SHI_TO_MONTH = {
        '寅': 2, '卯': 3, '辰': 4, '巳': 5, '午': 6, '未': 7,
        '申': 8, '酉': 9, '戌': 10, '亥': 11, '子': 12, '丑': 1
    }
    year = birth_date.year
    month = SHI_TO_MONTH[shi]
    
    # 未の地支の場合、前年の7月の節入り日を参照
    if shi == '未' and birth_date.month < 7:
        year -= 1
    
    # 丑月（1月）の場合、前年の節入り日
    if shi == '丑' and birth_date.month == 1:
        year -= 1
        
    setsuiri = get_setsuiri_date(datetime.datetime(year, month, 1))
    return (birth_date - setsuiri).days

# 天中殺の計算
def check_tenchuu_period(birth_date, tenchuu_type):
    """
    天中殺期間をチェック（毎年の該当期間）
    """
    TENCHUU_MONTHS = {
        '子丑天中殺': ['子月', '丑月'],  # 11月、12月
        '寅卯天中殺': ['寅月', '卯月'],  # 1月、2月  
        '辰巳天中殺': ['辰月', '巳月'],  # 3月、4月
        '午未天中殺': ['午月', '未月'],  # 5月、6月
        '申酉天中殺': ['申月', '酉月'],  # 7月、8月
        '戌亥天中殺': ['戌月', '亥月']   # 9月、10月
    }
    
    return TENCHUU_MONTHS.get(tenchuu_type, []) 

# 六十干支リスト（甲子～癸亥、正しい順番で明示的に定義）
ROKUJUKKANSHI = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
]

def get_nikkanshi_number(nikkanshi):
    """日干支（例：甲子）から六十干支番号（1～60）を返す"""
    try:
        return ROKUJUKKANSHI.index(nikkanshi) + 1
    except ValueError:
        return None

def get_tenchuu_by_nikkanshi(nikkanshi):
    """日干支から天中殺を判定"""
    num = get_nikkanshi_number(nikkanshi)
    if num is None:
        return ''
    if 1 <= num <= 10:
        return '戌亥天中殺'
    elif 11 <= num <= 20:
        return '申酉天中殺'
    elif 21 <= num <= 30:
        return '午未天中殺'
    elif 31 <= num <= 40:
        return '辰巳天中殺'
    elif 41 <= num <= 50:
        return '寅卯天中殺'
    elif 51 <= num <= 60:
        return '子丑天中殺'
    return '' 

# 節入りカレンダーを読み込む
def load_setsuiri_calendar():
    try:
        return pd.read_csv('meishiki_calculator/setsuiri_calendar.csv')
    except Exception as e:
        print(f"節入りカレンダーの読み込みエラー: {e}")
        return None

# 指定された年の節入り日付を取得
def get_setsuiri_dates(year):
    calendar = load_setsuiri_calendar()
    if calendar is None:
        return None
    
    year_data = calendar[calendar['year'] == year]
    if year_data.empty:
        return None
    
    return {
        'shokan': datetime.datetime.strptime(year_data['shokan'].iloc[0], '%Y-%m-%d'),
        'risshun': datetime.datetime.strptime(year_data['risshun'].iloc[0], '%Y-%m-%d'),
        'keichitsu': datetime.datetime.strptime(year_data['keichitsu'].iloc[0], '%Y-%m-%d'),
        'seimei': datetime.datetime.strptime(year_data['seimei'].iloc[0], '%Y-%m-%d'),
        'rikka': datetime.datetime.strptime(year_data['rikka'].iloc[0], '%Y-%m-%d'),
        'boshu': datetime.datetime.strptime(year_data['boshu'].iloc[0], '%Y-%m-%d'),
        'shosho': datetime.datetime.strptime(year_data['shosho'].iloc[0], '%Y-%m-%d'),
        'rikka2': datetime.datetime.strptime(year_data['rikka2'].iloc[0], '%Y-%m-%d'),
        'hakuro': datetime.datetime.strptime(year_data['hakuro'].iloc[0], '%Y-%m-%d'),
        'kanro': datetime.datetime.strptime(year_data['kanro'].iloc[0], '%Y-%m-%d'),
        'rittou': datetime.datetime.strptime(year_data['rittou'].iloc[0], '%Y-%m-%d'),
        'taisetsu': datetime.datetime.strptime(year_data['taisetsu'].iloc[0], '%Y-%m-%d')
    }

# 節入りからの日数を計算（改善版）
def get_days_from_setsuiri_for_shi(birth_date, shi):
    if isinstance(birth_date, datetime.datetime):
        birth_date = birth_date.date()
    
    year = birth_date.year
    setsuiri_dates = get_setsuiri_dates(year)
    
    if setsuiri_dates is None:
        return 0
    
    # 地支に対応する節入りを取得
    shi_to_setsuiri = {
        '子': 'risshun',    # 立春
        '丑': 'keichitsu',  # 啓蟄
        '寅': 'seimei',     # 清明
        '卯': 'rikka',      # 立夏
        '辰': 'boshu',      # 芒種
        '巳': 'shosho',     # 小暑
        '午': 'rikka2',     # 立秋
        '未': 'hakuro',     # 白露
        '申': 'kanro',      # 寒露
        '酉': 'rittou',     # 立冬
        '戌': 'taisetsu',   # 大雪
        '亥': 'shokan'      # 小寒
    }
    
    setsuiri_name = shi_to_setsuiri.get(shi)
    if setsuiri_name is None:
        return 0
    
    setsuiri_date = setsuiri_dates[setsuiri_name].date()
    
    # 日数計算
    days = (birth_date - setsuiri_date).days
    
    # 負の値の場合は次の年の節入りから計算
    if days < 0:
        next_year_setsuiri = get_setsuiri_dates(year + 1)
        if next_year_setsuiri is not None:
            next_setsuiri_date = next_year_setsuiri[setsuiri_name].date()
            days = (birth_date - next_setsuiri_date).days
    
    return days 
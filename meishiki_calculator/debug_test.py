from datetime import datetime as dt
from meishiki_calculator.kanshi_data import get_setsuiri_date, get_days_from_setsuiri_for_shi, get_main_zokan

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
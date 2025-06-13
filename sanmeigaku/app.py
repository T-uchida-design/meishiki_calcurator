from flask import Flask, request, jsonify
from destiny import Destiny
from kanshi_data import (
    calculate_eto, calculate_month_eto, calculate_day_eto,
    get_juusei, get_juunisei, get_main_zokan, get_days_from_setsuiri_for_shi,
    get_tenchuu_by_nikkanshi, check_tenchuu_period, JUUSEI_TABLE, JUUNISEI_TABLE
)

app = Flask(__name__)

@app.route('/api/meishiki', methods=['GET'])
def meishiki():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    day = int(request.args.get('day'))
    gender = request.args.get('gender', 'male')  # 'male' or 'female'

    d = Destiny(year, month, day, gender)
    result = d.get_bazi()  # 命式を取得
    return jsonify(result)

if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from meishiki_calculator.kanshi_data import convert_to_wareki

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        birth_date = request.json.get('birth_date')
        birth_time = request.json.get('birth_time')
        
        # 日付と時刻を結合してdatetimeオブジェクトを作成
        birth_datetime = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        
        # 和暦に変換
        wareki = convert_to_wareki(birth_datetime)
        
        # ここに命式計算のロジックを追加
        
        return jsonify({
            'success': True,
            'wareki': wareki,
            # 他の計算結果もここに追加
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 
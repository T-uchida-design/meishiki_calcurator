import streamlit as st
import pandas as pd
import datetime
from kanshi_data import (
    calculate_eto, calculate_month_eto, calculate_day_eto,
    get_juusei, get_juunisei, get_main_zokan, get_days_from_setsuiri_for_shi,
    get_tenchuu_by_nikkanshi, check_tenchuu_period, JUUSEI_TABLE, JUUNISEI_TABLE
)

# ページ設定
st.set_page_config(
    page_title="算命学 命式計算システム",
    page_icon="🔮",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
.main-title {
    text-align: center;
    color: #2E86AB;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
.section-title {
    color: #A23B72;
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #F18F01;
    padding-bottom: 0.5rem;
}
.human-chart {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    max-width: 400px;
    margin: 0 auto;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}
.chart-cell {
    background: rgba(255, 255, 255, 0.9);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    color: #2E86AB;
    border: 2px solid #F18F01;
    transition: transform 0.3s ease;
}
.chart-cell:hover {
    transform: scale(1.05);
}
.chart-center {
    background: linear-gradient(135deg, #F18F01 0%, #C73E1D 100%);
    color: white;
    font-size: 1.2rem;
}
.inyo-table {
    background: rgba(174, 207, 242, 0.2);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
.tenchuu-info {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def calculate_meishiki(birth_date):
    """命式を計算する"""
    try:
        # birth_dateがdate型ならdatetime型に変換
        if isinstance(birth_date, datetime.date) and not isinstance(birth_date, datetime.datetime):
            birth_date = datetime.datetime.combine(birth_date, datetime.time())

        # 干支計算
        eto_nen = calculate_eto(birth_date)
        eto_getsu = calculate_month_eto(birth_date)
        eto_nichi = calculate_day_eto(birth_date)

        nen_kan, nen_shi = eto_nen[0], eto_nen[1]
        getsu_kan, getsu_shi = eto_getsu[0], eto_getsu[1]
        nichi_kan, nichi_shi = eto_nichi[0], eto_nichi[1]

        # 日数計算（改善版）
        days_nen = get_days_from_setsuiri_for_shi(birth_date, nen_shi)
        days_getsu = get_days_from_setsuiri_for_shi(birth_date, getsu_shi)
        days_nichi = get_days_from_setsuiri_for_shi(birth_date, nichi_shi)

        # 主蔵干計算
        main_zokan_nen = get_main_zokan(nen_shi, days_nen)
        main_zokan_getsu = get_main_zokan(getsu_shi, days_getsu)
        main_zokan_nichi = get_main_zokan(nichi_shi, days_nichi)

        # 陽占計算（人体図）
        star_1 = get_juusei(nichi_kan, nen_kan)        # ①位置
        star_2 = get_juusei(nichi_kan, getsu_kan)      # ②位置
        star_3 = get_juusei(nichi_kan, main_zokan_getsu)  # ③位置（中心）
        star_4 = get_juusei(nichi_kan, main_zokan_nen)    # ④位置
        star_5 = get_juusei(nichi_kan, main_zokan_nichi)  # ⑤位置

        star_a = get_juunisei(nichi_kan, nen_shi)      # a位置
        star_b = get_juunisei(nichi_kan, getsu_shi)    # b位置
        star_c = get_juunisei(nichi_kan, nichi_shi)    # c位置

        # 天中殺計算（日干支で判定）
        nikkanshi = eto_nichi  # 例: '甲子'
        tenchuu = get_tenchuu_by_nikkanshi(nikkanshi)
        tenchuu_periods = check_tenchuu_period(birth_date, tenchuu)

        return {
            'nen_kan': nen_kan, 'nen_shi': nen_shi, 'main_zokan_nen': main_zokan_nen,
            'getsu_kan': getsu_kan, 'getsu_shi': getsu_shi, 'main_zokan_getsu': main_zokan_getsu,
            'nichi_kan': nichi_kan, 'nichi_shi': nichi_shi, 'main_zokan_nichi': main_zokan_nichi,
            'tenchuu': tenchuu, 'tenchuu_periods': tenchuu_periods,
            'stars': {
                '1': star_1, '2': star_2, '3': star_3, '4': star_4, '5': star_5,
                'a': star_a, 'b': star_b, 'c': star_c
            }
        }
    except Exception as e:
        st.error(f"計算エラー: {str(e)}")
        return None

def display_human_chart(stars, nichi_kan):
    """人体図をStreamlitの表形式で正しい配置・白い枠線付き・ラベル付きで表示する（位置説明はカット）"""
    st.markdown('<div class="section-title">🌟 陽占（人体図）</div>', unsafe_allow_html=True)

    # ラベル定義
    labels = {
        '1': '頭', 'a': '右手', '5': '左手', '3': '中年', '4': '右手',
        'c': '足', '2': '初年', 'b': '晩年'
    }
    # 3x3の人体図をst.columnsで再現（左上は空白、白い枠線付き、ラベル付き）
    cell_style = "background:rgba(255,255,255,0.07);border:2px solid #fff;border-radius:8px;padding:8px;text-align:center;font-weight:bold;min-height:40px;"
    center_style = cell_style + "background:#F18F01;color:white;"
    label_style = "font-size:0.8em;color:#fff;opacity:0.7;"

    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)

    with row1[0]:
        st.markdown(f"<div style='{cell_style}'></div>", unsafe_allow_html=True)  # 左上は空白
    with row1[1]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>頭</span><br>{stars['1']}</div>", unsafe_allow_html=True)
    with row1[2]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>右手</span><br>{stars['a']}</div>", unsafe_allow_html=True)

    with row2[0]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>左手</span><br>{stars['5']}</div>", unsafe_allow_html=True)
    with row2[1]:
        st.markdown(f"<div style='{center_style}'><span style='{label_style}'>中年</span><br>{stars['3']}<br>({nichi_kan})</div>", unsafe_allow_html=True)
    with row2[2]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>右手</span><br>{stars['4']}</div>", unsafe_allow_html=True)

    with row3[0]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>足</span><br>{stars['c']}</div>", unsafe_allow_html=True)
    with row3[1]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>初年</span><br>{stars['2']}</div>", unsafe_allow_html=True)
    with row3[2]:
        st.markdown(f"<div style='{cell_style}'><span style='{label_style}'>晩年</span><br>{stars['b']}</div>", unsafe_allow_html=True)

def display_star_descriptions():
    """星の説明＋人体図部位・年期の意味を表示する"""
    st.markdown('<div class="section-title">📚 十大主星の特徴</div>', unsafe_allow_html=True)
    star_descriptions = {
        '貫索星': '🔒 マイペース、独立心旺盛、職人気質',
        '石門星': '🤝 協調性、チームワーク、仲間意識',
        '鳳閣星': '🎭 自由奔放、芸術的才能、楽天的',
        '調舒星': '🎨 繊細、芸術性、美的感覚',
        '禄存星': '💰 引力本能、魅力的、商才',
        '司禄星': '💼 堅実、責任感、管理能力',
        '車騎星': '⚔️ 行動力、チャレンジ精神、リーダー',
        '牽牛星': '👑 名誉心、プライド、完璧主義',
        '龍高星': '🐉 革新的、変革者、直感力',
        '玉堂星': '📖 知識欲、学習能力、伝統重視'
    }
    cols = st.columns(2)
    for i, (star, desc) in enumerate(star_descriptions.items()):
        with cols[i % 2]:
            st.markdown(f"**{star}**: {desc}")

    # 部位・年期の意味
    st.markdown('<div class="section-title">🧑‍🦱 人体図の部位・年期の意味</div>', unsafe_allow_html=True)
    st.markdown("""
    - **頭**：知性や思考、判断力
    - **右手**：社会性、外向きの行動、対人関係
    - **左手**：家庭や内面、プライベート、感情
    - **足**：基盤、安定、現実的な行動
    - **初年**：若年期の運勢や傾向
    - **中年**：中年期の運勢や傾向
    - **晩年**：晩年期の運勢や傾向
    """)

def get_main_zokan(shi, days_from_setsuiri):
    if shi == '子':
        return '癸'
    elif shi == '丑':
        if days_from_setsuiri <= 9:
            return '癸'
        elif 10 <= days_from_setsuiri <= 12:
            return '辛'
        else:
            return '己'
    elif shi == '寅':
        if days_from_setsuiri <= 7:
            return '戊'
        elif 8 <= days_from_setsuiri <= 14:
            return '丙'
        else:
            return '甲'
    elif shi == '卯':
        return '乙'
    elif shi == '辰':
        if days_from_setsuiri <= 9:
            return '乙'
        elif 10 <= days_from_setsuiri <= 12:
            return '癸'
        else:
            return '戊'
    elif shi == '巳':
        if days_from_setsuiri <= 5:
            return '戊'
        elif 6 <= days_from_setsuiri <= 14:
            return '庚'
        else:
            return '丙'
    elif shi == '午':
        if days_from_setsuiri <= 19:
            return '己'
        else:
            return '丁'
    elif shi == '未':
        if days_from_setsuiri <= 9:
            return '丁'
        elif 10 <= days_from_setsuiri <= 12:
            return '乙'
        else:
            return '己'
    elif shi == '申':
        if days_from_setsuiri <= 10:
            return '戊'
        elif 11 <= days_from_setsuiri <= 13:
            return '壬'
        else:
            return '庚'
    elif shi == '酉':
        return '辛'
    elif shi == '戌':
        if days_from_setsuiri <= 9:
            return '辛'
        elif 10 <= days_from_setsuiri <= 12:
            return '丁'
        else:
            return '戊'
    elif shi == '亥':
        if days_from_setsuiri <= 12:
            return '甲'
        else:
            return '壬'
    return ''

def main():
    # タイトル
    st.markdown('<h1 class="main-title">🔮 算命学 命式計算システム</h1>', unsafe_allow_html=True)
    
    # サイドバー
    st.sidebar.markdown("## 📅 生年月日入力")
    
    # 生年月日入力
    birth_date = st.sidebar.date_input(
        "生年月日を選択してください",
        value=datetime.date(1990, 1, 1),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today()
    )
    
    # 性別選択（新規追加）
    gender = st.sidebar.radio("性別を選択してください", ("男", "女", "その他"))
    
    # 計算ボタン
    if st.sidebar.button("🔮 命式を計算", type="primary"):
        if birth_date:
            result = calculate_meishiki(birth_date)
            
            if result:
                # 結果の保存
                st.session_state['result'] = result
                st.session_state['birth_date'] = birth_date
                st.session_state['gender'] = gender
    
    # 結果表示
    if 'result' in st.session_state:
        result = st.session_state['result']
        birth_date = st.session_state['birth_date']
        gender = st.session_state['gender']
        
        # ヘッダー
        st.markdown("## 🌟 あなたの命式")
        st.markdown(f"**生年月日**: {birth_date.strftime('%Y年%m月%d日')}")
        st.markdown(f"**性別**: {gender}")
        
        # メインコンテンツ
        tab1, tab2, tab3 = st.tabs(["📊 命式詳細", "🌟 人体図", "📚 星の説明"])
        
        with tab1:
            # 陰占
            st.markdown('<div class="section-title">☯️ 陰占（干支・蔵干・主蔵干）</div>', unsafe_allow_html=True)
            
            inyo_df = pd.DataFrame({
                '日柱': [result['nichi_kan'], result['nichi_shi'], result['main_zokan_nichi']],
                '月柱': [result['getsu_kan'], result['getsu_shi'], result['main_zokan_getsu']],
                '年柱': [result['nen_kan'], result['nen_shi'], result['main_zokan_nen']]
            }, index=['天干', '地支', '主蔵干'])
            
            st.markdown('<div class="inyo-table">', unsafe_allow_html=True)
            st.dataframe(inyo_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 天中殺
            st.markdown('<div class="section-title">⚡ 天中殺</div>', unsafe_allow_html=True)
            tenchuu_html = f"""
            <div class="tenchuu-info">
                <h4>🎯 運命天中殺: {result['tenchuu']}</h4>
                <p>📅 毎年の天中殺期間: {', '.join(result['tenchuu_periods'])}</p>
                <p>💡 天中殺は、運気が不安定になりやすく、予想外の出来事やトラブルが起こりやすい時期です。<br>
                新しいことを始めるのは避け、現状維持や慎重な行動が推奨されます。</p>
            </div>
            """
            st.markdown(tenchuu_html, unsafe_allow_html=True)
        
        with tab2:
            # 人体図表示
            display_human_chart(result['stars'], result['nichi_kan'])
        
        with tab3:
            # 星の説明
            display_star_descriptions()
    
    else:
        # 初期画面
        st.markdown("### 🎯 算命学とは")
        st.markdown("""
        算命学は古代中国から伝わる占術で、生年月日から人の宿命や運命を読み解きます。
        
        **このシステムでできること:**
        - 📊 **陰占**: 干支・蔵干・主蔵干の算出
        - 🌟 **陽占**: 人体図（十大主星・十二大従星）の作成
        - ⚡ **天中殺**: 運命天中殺の判定
        
        左のサイドバーから生年月日を入力して、あなたの命式を見てみましょう！
        """)
        
        # サンプル表示
        st.markdown("### 🔮 人体図のサンプル")
        sample_stars = {
            '1': '龍高星', '2': '玉堂星', '3': '石門星', '4': '牽牛星', '5': '調舒星',
            'a': '天庫星', 'b': '天恍星', 'c': '天将星'
        }
        display_human_chart(sample_stars, '甲')

if __name__ == "__main__":
    main() 
# 命式計算システム

このプロジェクトは、生年月日と時刻から命式を計算するWebアプリケーションです。

## 機能

- 生年月日と時刻の入力
- 和暦への変換
- 命式の計算（干支、五行など）
- 結果の表示

## セットアップ

1. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

2. アプリケーションの実行:
```bash
python app.py
```

3. ブラウザで `http://localhost:5000` にアクセス

## テスト

テストの実行:
```bash
python -m pytest tests/
```

## プロジェクト構造

```
meishiki_calculator/
├── app.py              # メインアプリケーションファイル
├── requirements.txt    # 必要なパッケージのリスト
├── static/            # 静的ファイル
│   ├── css/          # スタイルシート
│   └── js/           # JavaScriptファイル
├── templates/         # HTMLテンプレート
└── tests/            # テストファイル
``` 
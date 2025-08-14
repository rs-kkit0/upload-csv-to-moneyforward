# upload-csv-to-moneyforward

[マネーフォワード家計簿](https://moneyforward.com/)に、CSVファイルをアップロードするためのPythonスクリプト群です。

## 概要

このプロジェクトは、マネーフォワード家計簿への家計データの一括登録を自動化するツールです。Seleniumを使用してブラウザ操作を自動化し、CSVファイルから家計データを読み込んでマネーフォワードに登録します。

## 機能

- **CSVアップロード機能** (`moneyforward.py`): CSVファイルから家計データを読み込み、マネーフォワードに自動登録
- **レポート生成機能** (`moneyforwardreport.py`): 指定した月の家計レポートを生成し、精算計算を自動化
- **カテゴリマッピング**: 分類と区分に基づいて、マネーフォワードのカテゴリを自動設定

## 必要な環境

- Python 3.7以上
- Chrome ブラウザ
- ChromeDriver

## インストール

1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/upload-csv-to-moneyforward.git
cd upload-csv-to-moneyforward
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. ChromeDriverをインストール
   - [ChromeDriver公式サイト](https://chromedriver.chromium.org/)からダウンロード
   - システムのPATHに追加するか、プロジェクトフォルダに配置

## セットアップ

### 1. 設定ファイルの準備

`settings.template.py`を`settings.py`にコピーし、認証情報を設定してください：

```bash
cp settings.template.py settings.py
```

`settings.py`を編集：
```python
user = "your-email@example.com"
password = "your-password"
```

### 2. カテゴリマッピングの設定

`mapping.template.py`を`mapping.py`にコピーし、必要に応じてカテゴリマッピングをカスタマイズしてください：

```bash
cp mapping.template.py mapping.py
```

### 3. CSVファイルの準備

CSVファイルは以下の形式で準備してください：

```csv
日時,店舗,金額,分類,区分
2023/08/11,スーパーA,1500,食費,夫負担
2023/08/12,コンビニB,300,日用品,妻負担
```

**CSVの列構成：**
- 1列目: 日時 (YYYY/MM/DD形式)
- 2列目: 店舗名
- 3列目: 金額
- 4列目: 分類 (食費、日用品、交際費など)
- 5列目: 区分 (夫負担、妻負担、割り勘など)

## 使用方法

### CSVアップロード

```bash
python moneyforward.py your-data.csv
```

**注意事項：**
- 初回実行時は、ログイン完了後にEnterキーを押してください
- ブラウザが自動で操作されるため、操作中は他の作業を避けてください
- 大量のデータを処理する場合は、処理時間がかかる場合があります

### レポート生成

```bash
python moneyforwardreport.py 202312
```

**パラメータ：**
- 年月を8桁の数字で指定 (例: 202312 = 2023年12月)

## ファイル構成

```
upload-csv-to-moneyforward/
├── moneyforward.py          # メインのCSVアップロードスクリプト
├── moneyforwardreport.py    # レポート生成スクリプト
├── mapping.template.py      # カテゴリマッピングテンプレート
├── settings.template.py     # 設定ファイルテンプレート
├── test.template.csv        # CSVファイルテンプレート
├── requirements.txt         # Python依存関係
└── README.md               # このファイル
```

READMEを大幅に整備いたしました。主な改善点は以下の通りです：

1. **詳細な概要説明**: プロジェクトの目的と機能を明確に記載
2. **インストール手順**: 段階的なセットアップ手順を追加
3. **使用方法**: 具体的なコマンド例と注意事項を記載
4. **ファイル構成**: 各ファイルの役割を説明
5. **カスタマイズ方法**: カテゴリマッピングの追加方法を説明
6. **トラブルシューティング**: よくある問題と解決方法を記載
7. **セキュリティ注意事項**: 認証情報の取り扱いについて説明
8. **サポート情報**: 問題発生時の対応方法を記載

これで、ユーザーがプロジェクトを理解し、適切にセットアップして使用できるようになります。

## カスタマイズ

### カテゴリマッピングの追加

`mapping.py`に新しいカテゴリマッピングを追加できます：

```python
category_mapping = {
    ("食費", "夫負担"): {"large_category_id": 11, "middle_category_id": 105},
    ("食費", "妻負担"): {"large_category_id": 11, "middle_category_id": 1101},
    # 新しいマッピングを追加
    ("交通費", "夫負担"): {"large_category_id": 15, "middle_category_id": 200},
}
```

### カテゴリIDの確認方法

マネーフォワードの家計簿入力画面で、ブラウザの開発者ツールを使用してカテゴリIDを確認できます。

## トラブルシューティング

### よくある問題

1. **ChromeDriverが見つからない**
   - ChromeDriverがインストールされているか確認
   - システムのPATHに追加されているか確認

2. **ログインに失敗する**
   - `settings.py`の認証情報が正しいか確認
   - マネーフォワードのアカウントが有効か確認

3. **CSVファイルが読み込めない**
   - ファイルの文字エンコーディングがUTF-8か確認
   - CSVの列構成が正しいか確認

### ログの確認

スクリプト実行時にコンソールに出力されるログを確認してください。エラーメッセージが表示される場合は、その内容を確認して対応してください。

## セキュリティに関する注意

- `settings.py`には認証情報が含まれているため、Gitにコミットしないでください
- `.gitignore`に`settings.py`を追加することを推奨します
- パスワードは強固なものを使用し、定期的に変更してください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

バグ報告や機能改善の提案は、GitHubのIssuesまたはPull Requestsでお願いします。

## サポート

問題が発生した場合や質問がある場合は、GitHubのIssuesで報告してください。

---

**注意**: このツールは個人利用を目的としており、マネーフォワードの利用規約に従ってご利用ください。大量のデータを処理する場合は、マネーフォワードのサーバーに負荷をかけないよう適切な間隔を設けて実行してください。

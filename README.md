# MoneyForward CSV アップロード・レポート生成ツール

## セットアップ

### 1. 設定ファイルの準備

```bash
# テンプレートファイルをコピー
cp report_config.template.py report_config.py

# 個人の設定に合わせて編集
# - 精算項目のキーワード
# - 控除項目の名前と金額
# - その他の設定
```

### 2. 設定ファイルの編集例

`report_config.py`を開いて、以下の項目を個人の状況に合わせて編集してください：

#### 精算項目の設定
- `keywords`: 経費の分類に使用するキーワード
- `divisor`: 負担割合（1/2、1/3など）
- `rounding`: 計算方法（floor: 切り捨て、ceil: 切り上げ、round: 四捨五入）

#### 控除項目の設定
- `name`: 控除項目の名前
- `amount`: 控除金額
- `description`: 控除項目の説明

#### レポート設定
- `default_group`: デフォルトのグループ名
- `wait_time`: ページ遷移時の待機時間
- `rounding_unit`: 切り捨て単位（1000円単位など）

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## 使用方法

### レポート生成

```bash
# 前月のレポートを生成
python moneyforwardreport.py

# 指定月のレポートを生成
python moneyforwardreport.py 202403
```

### テスト実行

```bash
# テストを実行
python run_tests.py
```

## 設定のカスタマイズ

### 新しい精算項目の追加

`report_config.py`の`SETTLEMENT_ITEMS`に新しい項目を追加：

```python
"new_category": {
    "name": "新しい精算項目",
    "description": "説明",
    "keywords": ["キーワード1", "キーワード2"],
    "divisor": 4,
    "rounding": "floor"
}
```

### 新しい控除項目の追加

`FIXED_DEDUCTIONS`に新しい項目を追加：

```python
{
    "name": "新しい控除項目",
    "amount": 5000,
    "description": "説明"
}
```

## 注意事項

- `report_config.py`は個人情報を含むため、Gitにコミットしないでください
- テンプレートファイル（`*.template.py`）は変更せず、コピーしてから編集してください
- 設定変更後は、必ずテストを実行して動作を確認してください

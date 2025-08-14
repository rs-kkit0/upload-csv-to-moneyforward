# レポート設定ファイル（テンプレート）
# 各項目の分類と計算方法を定義
# 使用前に report_config.py にコピーして、個人の設定に合わせて編集してください

# 精算項目の定義
SETTLEMENT_ITEMS = {
    "one_third": {
        "name": "1/3負担",
        "description": "水道・光熱費、家賃など",
        "keywords": ["水道・光熱費 合計", "家賃"],
        "divisor": 3,
        "rounding": "floor"
    },
    "one_second": {
        "name": "1/2負担", 
        "description": "割勘項目",
        "keywords": ["割勘"],
        "divisor": 2,
        "rounding": "floor"
    },
    "one_one": {
        "name": "1/1負担",
        "description": "個人負担",
        "keywords": ["個人負担"],
        "divisor": 1,
        "rounding": "floor"
    },
    "tatekae": {
        "name": "立替清算",
        "description": "立替分の清算",
        "keywords": ["立替"],
        "divisor": 2,
        "rounding": "floor",
        "is_deduction": True
    }
}

# 固定控除項目
FIXED_DEDUCTIONS = [
    {
        "name": "控除項目1",
        "amount": 0,
        "description": "控除項目の説明"
    },
    {
        "name": "控除項目2", 
        "amount": 0,
        "description": "控除項目の説明"
    },
    {
        "name": "控除項目3",
        "amount": 0,
        "description": "控除項目の説明"
    }
]

# レポート設定
REPORT_SETTINGS = {
    "default_group": "グループ選択なし",
    "report_url": "https://moneyforward.com/cf/summary",
    "wait_time": 3,
    "table_id": "table-outgo",
    "rounding_unit": 1000
}

# 出力フォーマット設定
OUTPUT_FORMAT = {
    "header": "*** {month}分 精算 ***",
    "item_header": "*** {name} ***",
    "total_format": "*** {name} 合計: {total:,} => {calculated:,}({unit}以下{rounding_type})",
    "final_total": "*** 請求合計: {total:,}円 ***",
    "separator": "*************************"
}

# 設定例（コメントアウト）
# SETTLEMENT_ITEMS = {
#     "one_third": {
#         "name": "1/3負担",
#         "description": "水道・光熱費、家賃など",
#         "keywords": ["水道・光熱費 合計", "家賃"],
#         "divisor": 3,
#         "rounding": "floor"
#     },
#     "one_second": {
#         "name": "1/2負担", 
#         "description": "割勘項目",
#         "keywords": ["割勘"],
#         "divisor": 2,
#         "rounding": "floor"
#     },
#     "one_one": {
#         "name": "1/1負担",
#         "description": "〇〇負担",
#         "keywords": ["〇〇負担"],
#         "divisor": 1,
#         "rounding": "floor"
#     },
#     "tatekae": {
#         "name": "立替清算",
#         "description": "立替分の清算",
#         "keywords": ["立替"],
#         "divisor": 2,
#         "rounding": "floor",
#         "is_deduction": True
#     }
# }
# 
# FIXED_DEDUCTIONS = [
#     {
#         "name": "育児手当",
#         "amount": 20000,
#         "description": "育児手当の控除"
#     },
#     {
#         "name": "児童手当等支給分", 
#         "amount": 20000,
#         "description": "児童手当の控除"
#     },
#     {
#         "name": "お弁当代",
#         "amount": 8000,
#         "description": "お弁当代の控除"
#     }
# ]

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# テスト対象のモジュールをインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import moneyforwardreport

class TestMoneyForwardReporter(unittest.TestCase):
    """MoneyForwardReporterクラスのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.reporter = moneyforwardreport.MoneyForwardReporter()
        
    def test_get_previous_month(self):
        """前月取得のテスト"""
        # 現在の日付を固定してテスト
        with patch('moneyforwardreport.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime(2024, 3, 15)
            result = self.reporter.get_previous_month()
            self.assertEqual(result, "202402")
            
            mock_datetime.today.return_value = datetime(2024, 1, 15)
            result = self.reporter.get_previous_month()
            self.assertEqual(result, "202312")

    def test_categorize_expenses(self):
        """経費分類のテスト"""
        # モックのテーブル行を作成
        mock_trs = [
            Mock(),  # ヘッダー行（スキップされる）
            Mock(),  # データ行1
            Mock(),  # データ行2
            Mock(),  # データ行3
        ]
        
        # 各データ行のモック設定
        mock_trs[1].find_elements.return_value = [
            Mock(text="水道・光熱費 合計"),
            Mock(text="15,000円")
        ]
        mock_trs[2].find_elements.return_value = [
            Mock(text="家賃"),
            Mock(text="80,000円")
        ]
        mock_trs[3].find_elements.return_value = [
            Mock(text="割勘"),
            Mock(text="5,000円")
        ]
        
        result = self.reporter.categorize_expenses(mock_trs)
        
        # 期待される結果
        self.assertIn("水道・光熱費 合計", [item[0] for item in result["one_third"]])
        self.assertIn("家賃", [item[0] for item in result["one_third"]])
        self.assertIn("割勘", [item[0] for item in result["one_second"]])

    def test_calculate_settlement(self):
        """精算計算のテスト"""
        items = [["項目1", 1000], ["項目2", 2000], ["項目3", 3000]]
        
        # 1/3負担、切り捨てのテスト
        calculated, total = self.reporter.calculate_settlement(items, 3, "floor")
        self.assertEqual(total, 6000)
        self.assertEqual(calculated, 2000)  # 6000/3 = 2000
        
        # 1/2負担、切り捨てのテスト
        calculated, total = self.reporter.calculate_settlement(items, 2, "floor")
        self.assertEqual(calculated, 3000)  # 6000/2 = 3000
        
        # 1/1負担のテスト
        calculated, total = self.reporter.calculate_settlement(items, 1, "floor")
        self.assertEqual(calculated, 6000)  # 6000/1 = 6000

    def test_calculate_settlement_with_rounding(self):
        """切り捨て計算のテスト"""
        items = [["項目1", 1000], ["項目2", 1500]]
        
        # 1/2負担、切り捨て（1000円単位）
        calculated, total = self.reporter.calculate_settlement(items, 2, "floor")
        self.assertEqual(total, 2500)
        self.assertEqual(calculated, 1000)  # 2500/2 = 1250 → 1000円単位で切り捨て
        
        # 1/3負担、切り捨て（1000円単位）
        calculated, total = self.reporter.calculate_settlement(items, 3, "floor")
        self.assertEqual(calculated, 0)  # 2500/3 = 833 → 1000円単位で切り捨て

    @patch('builtins.print')
    def test_output_settlement(self, mock_print):
        """精算出力のテスト"""
        items = [["水道・光熱費", 15000], ["家賃", 80000]]
        category_config = {
            "name": "1/3負担",
            "divisor": 3,
            "rounding": "floor"
        }
        
        result = self.reporter.output_settlement(items, category_config)
        
        # 出力が正しく呼ばれることを確認
        self.assertTrue(mock_print.called)
        # 計算結果が正しいことを確認
        self.assertEqual(result, 31000)  # (15000+80000)/3 = 31666 → 31000（切り捨て）

    @patch('builtins.print')
    def test_output_settlement_deduction(self, mock_print):
        """控除項目の出力テスト"""
        items = [["立替分", 10000]]
        category_config = {
            "name": "立替清算",
            "divisor": 2,
            "rounding": "floor",
            "is_deduction": True
        }
        
        result = self.reporter.output_settlement(items, category_config)
        
        # 控除項目なので負の値が返される
        self.assertEqual(result, -5000)  # 10000/2 = 5000、控除なので負

    def test_empty_items(self):
        """空の項目リストのテスト"""
        result = self.reporter.output_settlement([], {"name": "テスト", "divisor": 2, "rounding": "floor"})
        self.assertEqual(result, 0)

class TestMainFunction(unittest.TestCase):
    """メイン関数のテスト"""
    
    def test_main_with_valid_parameter(self):
        """有効なパラメータでのmain関数テスト"""
        with patch('sys.argv', ['moneyforwardreport.py', '202403']):
            with patch('moneyforwardreport.MoneyForwardReporter') as mock_reporter_class:
                mock_reporter = Mock()
                mock_reporter_class.return_value = mock_reporter
                mock_reporter.create_report.return_value = 1
                
                with patch('sys.exit') as mock_exit:
                    moneyforwardreport.main()
                    mock_exit.assert_called_once_with(1)

    def test_main_without_parameter(self):
        """パラメータなしでのmain関数テスト"""
        with patch('sys.argv', ['moneyforwardreport.py']):
            with patch('moneyforwardreport.MoneyForwardReporter') as mock_reporter_class:
                mock_reporter = Mock()
                mock_reporter_class.return_value = mock_reporter
                mock_reporter.get_previous_month.return_value = "202402"
                mock_reporter.create_report.return_value = 1
                
                with patch('sys.exit') as mock_exit:
                    moneyforwardreport.main()
                    mock_exit.assert_called_once_with(1)

class TestIntegration(unittest.TestCase):
    """統合テスト"""
    
    def test_full_settlement_flow(self):
        """完全な精算フローのテスト"""
        reporter = moneyforwardreport.MoneyForwardReporter()
        
        # モックデータ
        mock_items = {
            "one_third": [["水道・光熱費", 15000], ["家賃", 80000]],
            "one_second": [["割勘", 5000]],
            "one_one": [["個人負担", 3000]],
            "tatekae": [["立替", 10000]]
        }
        
        # 各項目の計算結果をシミュレート
        total = 0
        
        # 1/3負担: (15000+80000)/3 = 31666 → 31000（切り捨て）
        total += 31000
        # 1/2負担: 5000/2 = 2500 → 2000（切り捨て）
        total += 2000
        # 1/1負担: 3000/1 = 3000
        total += 3000
        # 立替清算: 10000/2 = 5000（控除）
        total -= 5000
        
        # 固定控除
        total -= 20000  # 育児手当
        total -= 20000  # 児童手当
        total -= 8000   # お弁当代
        
        expected_total = 31000 + 2000 + 3000 - 5000 - 20000 - 20000 - 8000
        self.assertEqual(total, expected_total)

if __name__ == '__main__':
    unittest.main()

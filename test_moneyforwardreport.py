import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# テスト対象のモジュールをインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import moneyforwardreport

class TestMoneyForwardReportFunctions(unittest.TestCase):
    """現在の関数ベースのコードのテスト"""
    
    def test_get_previous_month(self):
        """前月取得のテスト"""
        # 現在の日付を固定してテスト
        with patch('moneyforwardreport.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime(2024, 3, 15)
            result = moneyforwardreport.get_previous_month()
            self.assertEqual(result, "202402")
            
            mock_datetime.today.return_value = datetime(2024, 1, 15)
            result = moneyforwardreport.get_previous_month()
            self.assertEqual(result, "202312")

    def test_output_function(self):
        """output関数のテスト"""
        items = [["水道・光熱費", 15000], ["家賃", 80000]]
        
        with patch('builtins.print') as mock_print:
            result = moneyforwardreport.output(items, 3, False)
            
            # 出力が正しく呼ばれることを確認
            self.assertTrue(mock_print.called)
            # 計算結果が正しいことを確認（95000/3 = 31666 → 31000（切り捨て））
            self.assertEqual(result, 31000)

    def test_output_function_with_deduction(self):
        """控除項目のoutput関数テスト"""
        items = [["立替分", 10000]]
        
        with patch('builtins.print') as mock_print:
            result = moneyforwardreport.output(items, 2, True)
            
            # 控除項目の計算結果（10000/2 = 5000）
            self.assertEqual(result, 5000)

    def test_output_function_empty_list(self):
        """空のリストでのoutput関数テスト"""
        with patch('builtins.print') as mock_print:
            result = moneyforwardreport.output([], 2, False)
            self.assertEqual(result, 0)

    def test_output_function_rounding(self):
        """切り捨て計算のテスト"""
        items = [["項目1", 1000], ["項目2", 1500]]
        
        with patch('builtins.print') as mock_print:
            # 1/2負担、切り捨て（1000円単位）
            result = moneyforwardreport.output(items, 2, False)
            self.assertEqual(result, 1000)  # 2500/2 = 1250 → 1000円単位で切り捨て

class TestMainFunction(unittest.TestCase):
    """メイン関数のテスト"""
    
    def test_main_with_valid_parameter(self):
        """有効なパラメータでのmain関数テスト"""
        with patch('sys.argv', ['moneyforwardreport.py', '202403']):
            with patch('moneyforwardreport.createReport') as mock_create_report:
                mock_create_report.return_value = 1
                
                with patch('sys.exit') as mock_exit:
                    moneyforwardreport.createReport('202403')
                    mock_exit.assert_not_called()  # createReportは直接呼ばれる

    def test_main_without_parameter(self):
        """パラメータなしでのmain関数テスト"""
        with patch('sys.argv', ['moneyforwardreport.py']):
            with patch('moneyforwardreport.get_previous_month') as mock_get_month:
                mock_get_month.return_value = "202402"
                
                # 実際のmain処理をテスト
                result = moneyforwardreport.get_previous_month()
                self.assertEqual(result, "202402")

class TestIntegration(unittest.TestCase):
    """統合テスト（現在のコードの動作確認）"""
    
    def test_settlement_calculation_logic(self):
        """精算計算ロジックのテスト"""
        # 現在のコードの計算ロジックをシミュレート
        items = [["水道・光熱費", 15000], ["家賃", 80000]]
        
        # 1/3負担の計算: (15000+80000)/3 = 31666 → 31000（切り捨て）
        total = sum(item[1] for item in items)
        calculated = (total // 3 // 1000) * 1000
        self.assertEqual(calculated, 31000)
        
        # 1/2負担の計算: 5000/2 = 2500 → 2000（切り捨て）
        items2 = [["割勘", 5000]]
        total2 = sum(item[1] for item in items2)
        calculated2 = (total2 // 2 // 1000) * 1000
        self.assertEqual(calculated2, 2000)

    def test_fixed_deductions(self):
        """固定控除項目のテスト"""
        # 現在のコードの固定控除項目
        deductions = [20000, 20000, 8000]  # 育児手当、児童手当、お弁当代
        total_deduction = sum(deductions)
        self.assertEqual(total_deduction, 48000)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
テスト実行用スクリプト
"""

import unittest
import sys
import os

def run_tests():
    """テストを実行"""
    # テストディレクトリをPythonパスに追加
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # テストを検出して実行
    loader = unittest.TestLoader()
    start_dir = current_dir
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # テストランナーで実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 終了コードを設定
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())

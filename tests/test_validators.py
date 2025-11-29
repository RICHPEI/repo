"""
驗證工具測試

測試檔案路徑和欄位驗證功能。
"""

import unittest
from pathlib import Path
import pandas as pd
import sys
import os

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import validate_columns


class TestValidators(unittest.TestCase):
    """驗證工具測試類別"""

    def test_validate_columns_success(self):
        """測試欄位驗證成功的情況"""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': [7, 8, 9]
        })

        # 應該不拋出異常
        try:
            validate_columns(df, ['A', 'B'])
        except ValueError:
            self.fail("validate_columns raised ValueError unexpectedly!")

    def test_validate_columns_failure(self):
        """測試欄位驗證失敗的情況"""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        # 應該拋出 ValueError
        with self.assertRaises(ValueError) as context:
            validate_columns(df, ['A', 'C'])

        self.assertIn('缺少以下必要欄位', str(context.exception))

    def test_validate_columns_empty_list(self):
        """測試空欄位列表"""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })

        # 空列表應該通過驗證
        try:
            validate_columns(df, [])
        except ValueError:
            self.fail("validate_columns raised ValueError unexpectedly!")


if __name__ == '__main__':
    unittest.main()

"""
資料處理器測試

測試資料讀取、清洗與儲存功能。
"""

import unittest
import pandas as pd
import sys
import os

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processor import remove_duplicate_records


class TestDataProcessor(unittest.TestCase):
    """資料處理器測試類別"""

    def setUp(self):
        """設定測試資料"""
        self.test_df = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-01', '2025-01-02', '2025-01-02'],
            'Machine No.': ['M001', 'M001', 'M002', 'M002'],
            'Product': ['A', 'A', 'B', 'C'],
            'Quantity': [10, 10, 20, 30]
        })

    def test_remove_duplicates_keep_first(self):
        """測試保留第一筆重複記錄"""
        result = remove_duplicate_records(
            self.test_df,
            ['Date', 'Machine No.'],
            'first'
        )

        # 應該只保留 3 筆記錄（第1、3、4筆）
        self.assertEqual(len(result), 3)
        self.assertEqual(result.iloc[0]['Product'], 'A')

    def test_remove_duplicates_keep_last(self):
        """測試保留最後一筆重複記錄"""
        result = remove_duplicate_records(
            self.test_df,
            ['Date', 'Machine No.'],
            'last'
        )

        # 應該只保留 3 筆記錄（第2、3、4筆）
        self.assertEqual(len(result), 3)

    def test_remove_duplicates_keep_none(self):
        """測試移除所有重複記錄"""
        result = remove_duplicate_records(
            self.test_df,
            ['Date', 'Machine No.'],
            False
        )

        # 應該只保留 2 筆記錄（第3、4筆，因為第1、2筆是重複的）
        self.assertEqual(len(result), 2)

    def test_remove_duplicates_no_duplicates(self):
        """測試沒有重複記錄的情況"""
        df = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-02', '2025-01-03'],
            'Machine No.': ['M001', 'M002', 'M003'],
            'Product': ['A', 'B', 'C']
        })

        result = remove_duplicate_records(df, ['Date', 'Machine No.'], 'first')

        # 應該保留所有 3 筆記錄
        self.assertEqual(len(result), 3)

    def test_remove_duplicates_invalid_column(self):
        """測試使用不存在的欄位"""
        with self.assertRaises(ValueError):
            remove_duplicate_records(
                self.test_df,
                ['NonExistentColumn'],
                'first'
            )

    def test_remove_duplicates_single_column(self):
        """測試單一欄位去重"""
        result = remove_duplicate_records(
            self.test_df,
            ['Date'],
            'first'
        )

        # 按日期去重，應該只保留 2 筆記錄
        self.assertEqual(len(result), 2)


class TestDataProcessorEdgeCases(unittest.TestCase):
    """資料處理器邊界測試"""

    def test_empty_dataframe(self):
        """測試空資料框"""
        df = pd.DataFrame()

        # 空資料框應該返回空資料框
        result = remove_duplicate_records(df, [], 'first')
        self.assertEqual(len(result), 0)

    def test_single_row_dataframe(self):
        """測試單行資料框"""
        df = pd.DataFrame({
            'A': [1],
            'B': [2]
        })

        result = remove_duplicate_records(df, ['A'], 'first')
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()

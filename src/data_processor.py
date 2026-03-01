"""
資料處理模組

提供 Excel 資料的讀取、清洗與儲存功能。
"""

import logging
from pathlib import Path
from typing import List, Literal

import pandas as pd

from utils.validators import validate_file_path, validate_columns


def load_excel_data(file_path: Path) -> pd.DataFrame:
    """
    從 Excel 檔案讀取資料。

    Args:
        file_path: Excel 檔案的路徑

    Returns:
        讀取的資料框

    Raises:
        FileNotFoundError: 當檔案不存在時
        ValueError: 當檔案為空或格式錯誤時
        Exception: 其他讀取錯誤

    Example:
        >>> df = load_excel_data(Path("data.xlsx"))
        >>> print(len(df))
    """
    logging.info(f"開始讀取檔案：{file_path}")

    # 驗證檔案路徑
    validate_file_path(file_path, must_exist=True)

    try:
        # 根據副檔名選擇適當的引擎
        file_suffix = file_path.suffix.lower()
        if file_suffix == '.xls':
            logging.debug("偵測到 .xls 格式，使用 xlrd 引擎")
            data_frame = pd.read_excel(file_path, engine='xlrd')
        elif file_suffix in ['.xlsx', '.xlsm']:
            logging.debug(f"偵測到 {file_suffix} 格式，使用 openpyxl 引擎")
            data_frame = pd.read_excel(file_path, engine='openpyxl')
        else:
            raise ValueError(
                f"不支援的檔案格式：{file_suffix}\n"
                f"支援的格式：.xlsx, .xlsm, .xls"
            )

        # 驗證資料不為空
        if data_frame.empty:
            raise ValueError("讀取的資料框為空，無資料可處理")

        logging.info(f"成功讀取資料，共 {len(data_frame):,} 筆記錄")
        logging.info(f"資料欄位：{list(data_frame.columns)}")
        logging.debug(
            f"資料框記憶體使用：{data_frame.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        )

        return data_frame

    except ValueError as e:
        logging.error(f"資料驗證錯誤：{e}")
        raise
    except Exception as e:
        logging.error(f"讀取檔案時發生錯誤：{e}")
        raise


def remove_duplicate_records(
    data_frame: pd.DataFrame,
    duplicate_check_columns: List[str],
    keep_strategy: Literal['first', 'last', False] = 'first'
) -> pd.DataFrame:
    """
    移除資料框中的重複記錄。

    Args:
        data_frame: 原始資料框
        duplicate_check_columns: 用於檢查重複的欄位列表
        keep_strategy: 保留策略
            - 'first': 保留第一筆出現的記錄（預設）
            - 'last': 保留最後一筆出現的記錄
            - False: 移除所有重複的記錄

    Returns:
        移除重複後的資料框

    Raises:
        ValueError: 當指定的欄位不存在時

    Example:
        >>> df = pd.DataFrame({'A': [1, 1, 2], 'B': [3, 3, 4]})
        >>> cleaned = remove_duplicate_records(df, ['A'], 'first')
        >>> len(cleaned)
        2
    """
    # 驗證欄位存在
    validate_columns(data_frame, duplicate_check_columns)

    original_record_count = len(data_frame)

    logging.info(f"開始移除重複記錄...")
    logging.info(f"檢查重複的依據欄位：{duplicate_check_columns}")
    logging.info(f"保留策略：{keep_strategy}")

    # 移除重複記錄（效能最佳化：使用 inplace=False 避免不必要的複製）
    cleaned_data_frame = data_frame.drop_duplicates(
        subset=duplicate_check_columns,
        keep=keep_strategy,
        ignore_index=True
    )

    # 計算移除的記錄數
    removed_count = original_record_count - len(cleaned_data_frame)
    removed_percentage = (
        (removed_count / original_record_count * 100)
        if original_record_count > 0
        else 0
    )

    logging.info(f"移除了 {removed_count:,} 筆重複記錄 ({removed_percentage:.2f}%)")
    logging.info(f"清理後剩餘 {len(cleaned_data_frame):,} 筆記錄")

    return cleaned_data_frame


def save_excel_data(
    data_frame: pd.DataFrame,
    output_file_path: Path,
    include_index: bool = False
) -> None:
    """
    將資料框儲存為 Excel 檔案。

    Args:
        data_frame: 要儲存的資料框
        output_file_path: 輸出檔案路徑
        include_index: 是否在輸出檔案中包含索引欄

    Returns:
        None

    Raises:
        PermissionError: 當沒有寫入權限時
        Exception: 儲存過程中的其他錯誤

    Example:
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> save_excel_data(df, Path("output.xlsx"))
    """
    logging.info(f"開始儲存清理後的資料...")

    try:
        # 確保輸出目錄存在
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

        # 將資料寫入 Excel 檔案（效能最佳化：指定引擎）
        data_frame.to_excel(
            output_file_path,
            index=include_index,
            engine='openpyxl'
        )

        file_size = output_file_path.stat().st_size / 1024**2
        logging.info(f"資料已成功儲存至：{output_file_path}")
        logging.info(f"檔案大小：{file_size:.2f} MB")

    except PermissionError as e:
        logging.error(f"沒有檔案寫入權限：{e}")
        raise
    except Exception as e:
        logging.error(f"儲存檔案時發生錯誤：{e}")
        raise

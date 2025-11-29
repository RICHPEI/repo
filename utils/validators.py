"""
驗證工具模組

提供檔案路徑和資料欄位的驗證功能。
"""

import logging
from pathlib import Path
from typing import List

import pandas as pd


def validate_file_path(
    file_path: Path,
    must_exist: bool = True
) -> None:
    """
    驗證檔案路徑的有效性。

    Args:
        file_path: 要驗證的檔案路徑
        must_exist: 是否要求檔案必須存在

    Returns:
        None

    Raises:
        FileNotFoundError: 當 must_exist=True 且檔案不存在時
        ValueError: 當路徑無效時

    Example:
        >>> validate_file_path(Path("data.xlsx"), must_exist=True)
    """
    if must_exist and not file_path.exists():
        raise FileNotFoundError(f"找不到檔案：{file_path.absolute()}")

    if must_exist and not file_path.is_file():
        raise ValueError(f"路徑不是有效的檔案：{file_path.absolute()}")

    logging.debug(f"檔案路徑驗證通過：{file_path}")


def validate_columns(
    data_frame: pd.DataFrame,
    required_columns: List[str]
) -> None:
    """
    驗證資料框中是否包含必要的欄位。

    Args:
        data_frame: 要驗證的資料框
        required_columns: 必須存在的欄位列表

    Returns:
        None

    Raises:
        ValueError: 當任何必要欄位不存在時

    Example:
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> validate_columns(df, ['A', 'B'])
    """
    missing_columns = [col for col in required_columns if col not in data_frame.columns]

    if missing_columns:
        available_columns = list(data_frame.columns)
        raise ValueError(
            f"資料中缺少以下必要欄位：{missing_columns}\n"
            f"可用的欄位有：{available_columns}"
        )

    logging.debug(f"欄位驗證通過：{required_columns}")

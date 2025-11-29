"""
日誌設定模組

提供應用程式的日誌系統設定功能。
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None
) -> None:
    """
    設定日誌系統，用於記錄程式執行過程。

    配置日誌格式包含時間戳記、日誌層級和訊息內容。
    可選擇性地將日誌輸出至檔案。

    Args:
        log_level: 日誌層級 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日誌檔案路徑，若為 None 則只輸出到 console

    Returns:
        None

    Example:
        >>> setup_logging("DEBUG", Path("app.log"))
        >>> logging.info("Application started")
    """
    handlers: List[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if log_file:
        # 確保日誌檔案的目錄存在
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
        force=True
    )

    logging.debug(f"日誌系統已初始化，層級：{log_level}")
    if log_file:
        logging.debug(f"日誌將輸出至：{log_file}")

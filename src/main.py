"""
主程式入口

資料清洗工具的主要執行程式。
"""

import logging
import sys
from pathlib import Path
from typing import Literal

from src.cli import parse_arguments
from src.data_processor import load_excel_data, remove_duplicate_records, save_excel_data
from utils.logger import setup_logging


def main() -> int:
    """
    主程式執行流程。

    執行步驟：
    1. 解析命令列參數
    2. 設定日誌系統
    3. 讀取原始資料
    4. 驗證必要欄位
    5. 移除重複記錄
    6. 儲存清理後的資料

    Returns:
        程式結束代碼（0: 成功, 1: 失敗）

    Example:
        >>> sys.exit(main())
    """
    try:
        # 步驟 1: 解析命令列參數
        args = parse_arguments()

        # 步驟 2: 設定日誌系統
        log_file_path = Path(args.log_file) if args.log_file else None
        setup_logging(args.log_level, log_file_path)

        logging.info("=" * 70)
        logging.info("資料清洗程式 v2.0 開始執行")
        logging.info("=" * 70)

        # 轉換路徑為 Path 物件並解析為絕對路徑
        input_path = Path(args.input).resolve()
        output_path = Path(args.output).resolve()

        # 檢查輸入和輸出檔案是否相同
        if input_path == output_path:
            logging.error("錯誤：輸入和輸出檔案不能相同")
            logging.error("這會導致原始資料被覆蓋，請指定不同的輸出檔案")
            return 1

        logging.info(f"輸入檔案：{input_path.absolute()}")
        logging.info(f"輸出檔案：{output_path.absolute()}")
        logging.info(f"重複檢查欄位：{args.columns}")
        logging.info(f"保留策略：{args.keep}")

        # 步驟 3: 讀取原始資料
        original_data = load_excel_data(input_path)

        # 顯示原始資料預覽（可選）
        if not args.no_preview:
            logging.info("\n原始資料前 5 筆預覽：")
            print(original_data.head())
            print()

        # 步驟 4 & 5: 移除重複記錄
        keep_strategy: Literal['first', 'last', False] = (
            False if args.keep == 'none' else args.keep  # type: ignore
        )
        cleaned_data = remove_duplicate_records(
            original_data,
            args.columns,
            keep_strategy
        )

        # 顯示清理後資料預覽（可選）
        if not args.no_preview:
            logging.info("\n清理後資料前 5 筆預覽：")
            print(cleaned_data.head())
            print()

        # 步驟 6: 儲存清理後的資料
        save_excel_data(cleaned_data, output_path, args.include_index)

        logging.info("=" * 70)
        logging.info("資料清洗程式執行完成！")
        logging.info("=" * 70)

        return 0

    except FileNotFoundError as e:
        logging.error(f"檔案錯誤：{e}")
        logging.error("請確認檔案路徑是否正確")
        return 1

    except ValueError as e:
        logging.error(f"數值錯誤：{e}")
        logging.error("請檢查欄位名稱或參數設定")
        return 1

    except PermissionError as e:
        logging.error(f"權限錯誤：{e}")
        logging.error("請確認有足夠的檔案讀寫權限")
        return 1

    except KeyboardInterrupt:
        logging.warning("\n程式被使用者中斷")
        return 130

    except Exception as e:
        logging.exception(f"發生未預期的錯誤：{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

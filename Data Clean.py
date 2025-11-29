"""
資料清洗腳本

此腳本用於清理 Excel 資料中的重複記錄，支援命令列參數設定。
提供完整的類型提示、日誌記錄、錯誤處理與效能最佳化。
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional, Literal

import pandas as pd

# ============================================================================
# 日誌設定
# ============================================================================

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


# ============================================================================
# 檔案驗證函式
# ============================================================================

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
    """
    if must_exist and not file_path.exists():
        raise FileNotFoundError(f"找不到檔案：{file_path.absolute()}")

    if must_exist and not file_path.is_file():
        raise ValueError(f"路徑不是有效的檔案：{file_path.absolute()}")


# ============================================================================
# 資料讀取函式
# ============================================================================

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
    """
    logging.info(f"開始讀取檔案：{file_path}")

    # 驗證檔案路徑
    validate_file_path(file_path, must_exist=True)

    try:
        # 根據檔案副檔名選擇適當的引擎
        file_extension = file_path.suffix.lower()

        if file_extension == '.xls':
            # 舊版 Excel 格式，使用 xlrd 引擎
            try:
                data_frame = pd.read_excel(file_path, engine='xlrd')
            except ImportError:
                raise ValueError(
                    "讀取 .xls 檔案需要安裝 xlrd 套件\n"
                    "請執行：pip install xlrd"
                )
        elif file_extension in ['.xlsx', '.xlsm']:
            # 新版 Excel 格式，使用 openpyxl 引擎
            data_frame = pd.read_excel(file_path, engine='openpyxl')
        else:
            raise ValueError(
                f"不支援的檔案格式：{file_extension}\n"
                f"支援的格式：.xlsx, .xlsm, .xls"
            )

        # 驗證資料不為空
        if data_frame.empty:
            raise ValueError("讀取的資料框為空，無資料可處理")

        logging.info(f"成功讀取資料，共 {len(data_frame):,} 筆記錄")
        logging.info(f"資料欄位：{list(data_frame.columns)}")
        logging.debug(f"資料框記憶體使用：{data_frame.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        return data_frame

    except ValueError as e:
        logging.error(f"資料驗證錯誤：{e}")
        raise
    except Exception as e:
        logging.error(f"讀取檔案時發生錯誤：{e}")
        raise


# ============================================================================
# 欄位驗證函式
# ============================================================================

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
    """
    missing_columns = [col for col in required_columns if col not in data_frame.columns]

    if missing_columns:
        available_columns = list(data_frame.columns)
        raise ValueError(
            f"資料中缺少以下必要欄位：{missing_columns}\n"
            f"可用的欄位有：{available_columns}"
        )

    logging.debug(f"欄位驗證通過：{required_columns}")


# ============================================================================
# 資料清洗函式
# ============================================================================

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
    removed_percentage = (removed_count / original_record_count * 100) if original_record_count > 0 else 0

    logging.info(f"移除了 {removed_count:,} 筆重複記錄 ({removed_percentage:.2f}%)")
    logging.info(f"清理後剩餘 {len(cleaned_data_frame):,} 筆記錄")

    return cleaned_data_frame


# ============================================================================
# 資料儲存函式
# ============================================================================

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


# ============================================================================
# 命令列參數解析
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """
    解析命令列參數。

    Returns:
        解析後的參數物件

    Raises:
        SystemExit: 當參數錯誤時
    """
    parser = argparse.ArgumentParser(
        description='Excel 資料清洗工具 - 移除重複記錄',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例：
  # 基本使用（使用預設欄位 Date 和 Machine No.）
  python "Data Clean.py" -i input.xlsx -o output.xlsx

  # 指定自訂欄位進行重複檢查
  python "Data Clean.py" -i data.xlsx -o clean.xlsx -c "Date" "Product ID"

  # 保留最後一筆重複記錄
  python "Data Clean.py" -i data.xlsx -o clean.xlsx -k last

  # 移除所有重複記錄（不保留任何一筆）
  python "Data Clean.py" -i data.xlsx -o clean.xlsx -k none

  # 啟用詳細日誌並儲存至檔案
  python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-level DEBUG --log-file cleaning.log

  # 在輸出中包含索引欄位
  python "Data Clean.py" -i data.xlsx -o clean.xlsx --include-index
        """
    )

    # 必要參數
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        metavar='FILE',
        help='輸入 Excel 檔案路徑（必要）'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        metavar='FILE',
        help='輸出 Excel 檔案路徑（必要）'
    )

    # 可選參數
    parser.add_argument(
        '-c', '--columns',
        type=str,
        nargs='+',
        default=['Date', 'Machine No.'],
        metavar='COL',
        help='用於判斷重複的欄位名稱（預設: Date "Machine No."）'
    )

    parser.add_argument(
        '-k', '--keep',
        type=str,
        choices=['first', 'last', 'none'],
        default='first',
        help='重複記錄的保留策略：first=保留第一筆, last=保留最後一筆, none=全部移除（預設: first）'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='日誌詳細程度（預設: INFO）'
    )

    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        metavar='FILE',
        help='日誌檔案路徑（若未指定則只輸出到終端機）'
    )

    parser.add_argument(
        '--include-index',
        action='store_true',
        help='在輸出檔案中包含索引欄位'
    )

    parser.add_argument(
        '--no-preview',
        action='store_true',
        help='不顯示資料預覽（加快處理速度）'
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )

    return parser.parse_args()


# ============================================================================
# 主程式
# ============================================================================

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

        # 轉換路徑為 Path 物件
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
        keep_strategy: Literal['first', 'last', False] = False if args.keep == 'none' else args.keep  # type: ignore
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


# ============================================================================
# 程式進入點
# ============================================================================

if __name__ == "__main__":
    sys.exit(main())
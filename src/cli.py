"""
命令列介面模組

提供命令列參數解析功能。
"""

import argparse


def parse_arguments() -> argparse.Namespace:
    """
    解析命令列參數。

    Returns:
        解析後的參數物件

    Raises:
        SystemExit: 當參數錯誤時

    Example:
        >>> args = parse_arguments()
        >>> print(args.input)
    """
    parser = argparse.ArgumentParser(
        description='Excel 資料清洗工具 - 移除重複記錄',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例：
  # 基本使用（使用預設欄位 Date 和 Machine No.）
  python -m src.main -i input.xlsx -o output.xlsx

  # 指定自訂欄位進行重複檢查
  python -m src.main -i data.xlsx -o clean.xlsx -c "Date" "Product ID"

  # 保留最後一筆重複記錄
  python -m src.main -i data.xlsx -o clean.xlsx -k last

  # 移除所有重複記錄（不保留任何一筆）
  python -m src.main -i data.xlsx -o clean.xlsx -k none

  # 啟用詳細日誌並儲存至檔案
  python -m src.main -i data.xlsx -o clean.xlsx --log-level DEBUG --log-file cleaning.log

  # 在輸出中包含索引欄位
  python -m src.main -i data.xlsx -o clean.xlsx --include-index
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

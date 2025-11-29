# Excel 資料清洗工具 v2.0

一個專業級的 Python 資料清洗工具，提供 Excel 檔案重複記錄移除功能，採用模組化設計、完整類型提示、命令列介面、詳細日誌記錄與完善的錯誤處理機制。

## 目錄

- [主要特色](#主要特色)
- [專案結構](#專案結構)
- [安裝說明](#安裝說明)
- [使用方法](#使用方法)
- [開發指南](#開發指南)
- [測試](#測試)
- [API 文件](#api-文件)

## 主要特色

### 🏗️ 架構設計
- **模組化架構**：功能職責明確分離
- **完整類型提示**：所有函式都有類型註解
- **命令列介面**：使用 argparse 提供靈活配置
- **零硬編碼**：所有設定皆可透過參數配置
- **單元測試**：包含完整的測試套件

### 🚀 效能最佳化
- **明確引擎指定**：使用 openpyxl 引擎
- **記憶體監控**：DEBUG 模式顯示記憶體使用
- **可選預覽**：大型資料集可關閉預覽加速
- **索引重置**：自動重置索引避免不連續

### 📝 日誌與錯誤處理
- **分級日誌系統**：DEBUG/INFO/WARNING/ERROR/CRITICAL
- **日誌檔案輸出**：支援同時輸出到檔案和終端機
- **詳細錯誤訊息**：針對不同錯誤類型提供處理建議
- **完整異常捕捉**：檔案、欄位、權限等錯誤

### 🎯 資料處理
- **智慧型重複檢測**：支援多欄位組合
- **彈性保留策略**：first/last/none 三種模式
- **欄位自動驗證**：檢查必要欄位存在性
- **統計資訊**：顯示移除數量與百分比

## 專案結構

```
excel-data-cleaner/
│
├── src/                        # 主要程式碼
│   ├── __init__.py            # 套件初始化
│   ├── main.py                # 主程式入口
│   ├── cli.py                 # 命令列介面
│   └── data_processor.py      # 資料處理核心
│
├── utils/                      # 工具模組
│   ├── __init__.py
│   ├── logger.py              # 日誌設定
│   └── validators.py          # 驗證工具
│
├── tests/                      # 測試檔案
│   ├── __init__.py
│   ├── test_validators.py     # 驗證工具測試
│   └── test_data_processor.py # 資料處理測試
│
├── Data Clean.py               # 舊版單檔程式（向下相容）
├── requirements.txt            # 依賴套件清單
├── .gitignore                 # Git 忽略規則
└── README.md                  # 專案說明文件
```

## 安裝說明

### 系統需求

- Python 3.7 或以上版本（建議 3.9+）
- pip 套件管理工具

### 安裝步驟

1. **複製專案**

```bash
git clone <repository-url>
cd excel-data-cleaner
```

2. **建立虛擬環境**（建議）

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **安裝依賴套件**

```bash
pip install -r requirements.txt
```

4. **驗證安裝**

```bash
python -m src.main --version
```

## 使用方法

### 基本語法

```bash
python -m src.main -i <輸入檔案> -o <輸出檔案> [選項]
```

### 必要參數

| 參數 | 說明 |
|------|------|
| `-i, --input FILE` | 輸入 Excel 檔案路徑 |
| `-o, --output FILE` | 輸出 Excel 檔案路徑 |

### 可選參數

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `-c, --columns COL [COL ...]` | Date "Machine No." | 用於判斷重複的欄位 |
| `-k, --keep {first,last,none}` | first | 重複記錄保留策略 |
| `--log-level LEVEL` | INFO | 日誌詳細程度 |
| `--log-file FILE` | None | 日誌檔案路徑 |
| `--include-index` | False | 包含索引欄位 |
| `--no-preview` | False | 不顯示資料預覽 |
| `-v, --version` | - | 顯示版本資訊 |
| `-h, --help` | - | 顯示說明訊息 |

### 使用範例

#### 1. 基本使用

```bash
python -m src.main -i input.xlsx -o output.xlsx
```

#### 2. 指定自訂欄位

```bash
python -m src.main -i data.xlsx -o clean.xlsx -c "訂單日期" "產品編號"
```

#### 3. 保留最後一筆

```bash
python -m src.main -i data.xlsx -o clean.xlsx -k last
```

#### 4. 移除所有重複

```bash
python -m src.main -i data.xlsx -o clean.xlsx -k none
```

#### 5. 啟用詳細日誌

```bash
python -m src.main -i data.xlsx -o clean.xlsx --log-level DEBUG --log-file app.log
```

#### 6. 處理大型檔案

```bash
python -m src.main -i large.xlsx -o clean.xlsx --no-preview
```

### 使用舊版程式（向下相容）

舊版單檔程式仍然可用：

```bash
python "Data Clean.py" -i input.xlsx -o output.xlsx
```

## 開發指南

### 設定開發環境

1. **安裝開發依賴**

取消 `requirements.txt` 中開發工具的註解並安裝：

```bash
pip install pytest pytest-cov mypy black flake8
```

2. **程式碼格式化**

```bash
black src/ utils/ tests/
```

3. **類型檢查**

```bash
mypy src/ utils/
```

4. **程式碼檢查**

```bash
flake8 src/ utils/ tests/
```

### 專案架構說明

#### src/ - 主要程式碼

- **main.py**: 主程式入口，協調各模組運作
- **cli.py**: 命令列參數解析
- **data_processor.py**: 核心資料處理邏輯

#### utils/ - 工具模組

- **logger.py**: 日誌系統設定
- **validators.py**: 資料驗證工具

#### tests/ - 測試檔案

- **test_validators.py**: 驗證工具測試
- **test_data_processor.py**: 資料處理測試

### 新增功能指南

1. **新增資料處理功能**
   - 在 `src/data_processor.py` 中新增函式
   - 在 `tests/test_data_processor.py` 中新增對應測試

2. **新增驗證規則**
   - 在 `utils/validators.py` 中新增驗證函式
   - 在 `tests/test_validators.py` 中新增測試

3. **新增命令列參數**
   - 在 `src/cli.py` 中的 `parse_arguments()` 新增參數
   - 在 `src/main.py` 中使用新參數

## 測試

### 執行所有測試

```bash
python -m pytest tests/
```

### 執行特定測試檔案

```bash
python -m pytest tests/test_validators.py
```

### 查看測試覆蓋率

```bash
python -m pytest --cov=src --cov=utils tests/
```

### 使用 unittest 執行測試

```bash
# 執行所有測試
python -m unittest discover tests/

# 執行特定測試
python -m unittest tests.test_validators
```

### 測試報告範例

```
tests/test_validators.py ......                                          [ 50%]
tests/test_data_processor.py .........                                   [100%]

==================== 15 passed in 0.45s ====================
```

## API 文件

### 資料處理器 (data_processor.py)

#### `load_excel_data(file_path: Path) -> pd.DataFrame`

從 Excel 檔案讀取資料。

**參數:**
- `file_path`: Excel 檔案路徑

**回傳:**
- `pd.DataFrame`: 讀取的資料框

**拋出異常:**
- `FileNotFoundError`: 檔案不存在
- `ValueError`: 檔案為空或格式錯誤

**範例:**
```python
from pathlib import Path
from src.data_processor import load_excel_data

df = load_excel_data(Path("data.xlsx"))
print(f"讀取了 {len(df)} 筆記錄")
```

#### `remove_duplicate_records(data_frame, duplicate_check_columns, keep_strategy='first')`

移除重複記錄。

**參數:**
- `data_frame`: 原始資料框
- `duplicate_check_columns`: 用於檢查重複的欄位列表
- `keep_strategy`: 保留策略 ('first'/'last'/False)

**回傳:**
- `pd.DataFrame`: 清理後的資料框

**範例:**
```python
cleaned_df = remove_duplicate_records(
    df,
    ['Date', 'Machine No.'],
    'first'
)
```

#### `save_excel_data(data_frame, output_file_path, include_index=False)`

儲存資料框為 Excel 檔案。

**參數:**
- `data_frame`: 要儲存的資料框
- `output_file_path`: 輸出檔案路徑
- `include_index`: 是否包含索引

**範例:**
```python
save_excel_data(cleaned_df, Path("output.xlsx"))
```

### 驗證工具 (validators.py)

#### `validate_file_path(file_path, must_exist=True)`

驗證檔案路徑。

#### `validate_columns(data_frame, required_columns)`

驗證資料框包含必要欄位。

### 日誌工具 (logger.py)

#### `setup_logging(log_level='INFO', log_file=None)`

設定日誌系統。

## 常見問題

### Q1: 如何處理中文欄位名稱？

直接使用引號包圍即可：

```bash
python -m src.main -i data.xlsx -o clean.xlsx -c "日期" "機台編號"
```

### Q2: 如何批次處理多個檔案？

建立 shell 腳本：

```bash
#!/bin/bash
for file in data/*.xlsx; do
    output="cleaned/$(basename "$file")"
    python -m src.main -i "$file" -o "$output" --no-preview
done
```

### Q3: 測試失敗怎麼辦？

確保已安裝所有依賴：

```bash
pip install -r requirements.txt
```

### Q4: 如何貢獻程式碼？

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 建立 Pull Request

## 版本歷史

### v2.0.0 (2025-11-29)
- ✨ 重構為模組化架構
- ✨ 新增完整類型提示
- ✨ 新增單元測試套件
- ✨ 新增命令列介面
- ✨ 改進錯誤處理
- ✨ 新增專案文件

### v1.0.0
- 基本資料清洗功能
- 單檔程式

## 授權

MIT License

## 作者

Data Cleaning Team

## 技術支援

- 建立 Issue
- 提交 Pull Request
- 查看 [Wiki](wiki/)
- 聯絡維護者

## 致謝

感謝所有貢獻者對本專案的支持！

---

**注意**: 本專案持續開發中，歡迎提供建議與回饋。

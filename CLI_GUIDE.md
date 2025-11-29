# Data Clean.py - CLI 使用指南

## 快速開始

### 安裝依賴
```bash
pip install pandas openpyxl
```

### 最簡單的使用方式
```bash
python "Data Clean.py" -i input.xlsx -o output.xlsx
```

## 完整參數說明

### 必要參數

#### `-i, --input FILE`
輸入 Excel 檔案路徑

**範例:**
```bash
python "Data Clean.py" -i data.xlsx -o clean.xlsx
python "Data Clean.py" -i "我的資料.xlsx" -o output.xlsx
python "Data Clean.py" -i /path/to/data.xlsx -o output.xlsx
```

#### `-o, --output FILE`
輸出 Excel 檔案路徑

**範例:**
```bash
python "Data Clean.py" -i input.xlsx -o output.xlsx
python "Data Clean.py" -i input.xlsx -o "清理後的資料.xlsx"
python "Data Clean.py" -i input.xlsx -o /path/to/output.xlsx
```

### 可選參數

#### `-c, --columns COL [COL ...]`
用於判斷重複的欄位名稱

**預設值:** `Date` `Machine No.`

**範例:**
```bash
# 使用單一欄位
python "Data Clean.py" -i data.xlsx -o clean.xlsx -c Date

# 使用多個欄位
python "Data Clean.py" -i data.xlsx -o clean.xlsx -c Date Product

# 中文欄位名稱
python "Data Clean.py" -i data.xlsx -o clean.xlsx -c "訂單日期" "產品編號"

# 混合中英文
python "Data Clean.py" -i data.xlsx -o clean.xlsx -c Date "產品編號" "客戶ID"
```

#### `-k, --keep {first,last,none}`
重複記錄的保留策略

**預設值:** `first`

**選項:**
- `first`: 保留第一筆出現的記錄
- `last`: 保留最後一筆出現的記錄
- `none`: 移除所有重複的記錄（一筆都不保留）

**範例:**
```bash
# 保留第一筆（預設）
python "Data Clean.py" -i data.xlsx -o clean.xlsx -k first

# 保留最後一筆
python "Data Clean.py" -i data.xlsx -o clean.xlsx -k last

# 全部移除
python "Data Clean.py" -i data.xlsx -o clean.xlsx -k none
```

#### `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}`
日誌詳細程度

**預設值:** `INFO`

**層級說明:**
- `DEBUG`: 最詳細，包含記憶體使用、欄位驗證等
- `INFO`: 標準資訊，顯示處理進度和統計
- `WARNING`: 只顯示警告和錯誤
- `ERROR`: 只顯示錯誤
- `CRITICAL`: 只顯示嚴重錯誤

**範例:**
```bash
# 詳細除錯資訊
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-level DEBUG

# 標準資訊（預設）
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-level INFO

# 只顯示警告
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-level WARNING
```

#### `--log-file FILE`
日誌檔案輸出路徑

**預設值:** 無（只輸出到終端機）

**範例:**
```bash
# 儲存日誌到檔案
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-file cleaning.log

# 搭配 DEBUG 層級
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-level DEBUG --log-file debug.log

# 使用日期時間作為檔名
python "Data Clean.py" -i data.xlsx -o clean.xlsx --log-file "log_$(date +%Y%m%d_%H%M%S).log"
```

#### `--include-index`
在輸出檔案中包含索引欄位

**預設值:** False（不包含）

**範例:**
```bash
# 包含索引欄位
python "Data Clean.py" -i data.xlsx -o clean.xlsx --include-index
```

#### `--no-preview`
不顯示資料預覽（加快處理速度）

**預設值:** False（會顯示預覽）

**適用情境:**
- 處理大型檔案時
- 批次處理多個檔案時
- 在腳本中自動化執行時

**範例:**
```bash
# 關閉預覽
python "Data Clean.py" -i large.xlsx -o clean.xlsx --no-preview
```

#### `-v, --version`
顯示程式版本資訊

**範例:**
```bash
python "Data Clean.py" --version
```

**輸出:**
```
Data Clean.py 2.0.0
```

#### `-h, --help`
顯示完整的說明訊息

**範例:**
```bash
python "Data Clean.py" --help
```

## 實用範例

### 範例 1: 基本清洗
清理包含日期和機器編號的資料

```bash
python "Data Clean.py" -i "DATA FROM ECOCO FOR HALF A YEAR.xlsx" -o "cleaned_data.xlsx"
```

### 範例 2: 自訂欄位清洗
使用訂單日期、產品編號和客戶ID三個欄位判斷重複

```bash
python "Data Clean.py" \
  -i orders.xlsx \
  -o orders_clean.xlsx \
  -c "訂單日期" "產品編號" "客戶ID"
```

### 範例 3: 保留最新資料
保留每組重複記錄中的最後一筆（最新的）

```bash
python "Data Clean.py" \
  -i transactions.xlsx \
  -o latest_transactions.xlsx \
  -c "客戶ID" "交易日期" \
  -k last
```

### 範例 4: 完全去重
移除所有重複的記錄，只保留唯一的記錄

```bash
python "Data Clean.py" \
  -i data.xlsx \
  -o unique_data.xlsx \
  -c "ID" \
  -k none
```

### 範例 5: 除錯模式
啟用詳細日誌並儲存到檔案，用於診斷問題

```bash
python "Data Clean.py" \
  -i problematic_data.xlsx \
  -o output.xlsx \
  --log-level DEBUG \
  --log-file debug_$(date +%Y%m%d).log
```

### 範例 6: 批次處理
處理目錄中的所有 Excel 檔案

```bash
#!/bin/bash
for file in data/*.xlsx; do
    filename=$(basename "$file" .xlsx)
    python "Data Clean.py" \
      -i "$file" \
      -o "cleaned/${filename}_clean.xlsx" \
      --no-preview \
      --log-file "logs/${filename}.log"
done
```

### 範例 7: 完整配置
使用所有可用選項的完整範例

```bash
python "Data Clean.py" \
  --input "原始資料/銷售記錄.xlsx" \
  --output "清理後資料/銷售記錄_已清洗.xlsx" \
  --columns "日期" "門市" "產品代碼" \
  --keep first \
  --log-level INFO \
  --log-file "logs/cleaning_$(date +%Y%m%d_%H%M%S).log" \
  --include-index
```

## 輸出範例

### 標準輸出 (INFO 層級)

```
2025-11-29 17:30:00 - INFO - ======================================================================
2025-11-29 17:30:00 - INFO - 資料清洗程式 v2.0 開始執行
2025-11-29 17:30:00 - INFO - ======================================================================
2025-11-29 17:30:00 - INFO - 輸入檔案：/Users/user/data/input.xlsx
2025-11-29 17:30:00 - INFO - 輸出檔案：/Users/user/data/output.xlsx
2025-11-29 17:30:00 - INFO - 重複檢查欄位：['Date', 'Machine No.']
2025-11-29 17:30:00 - INFO - 保留策略：first
2025-11-29 17:30:00 - INFO - 開始讀取檔案：/Users/user/data/input.xlsx
2025-11-29 17:30:01 - INFO - 成功讀取資料，共 1,500 筆記錄
2025-11-29 17:30:01 - INFO - 資料欄位：['Date', 'Machine No.', 'Product', 'Quantity']

原始資料前 5 筆預覽：
         Date Machine No. Product  Quantity
0  2025-01-01        M001       A        10
1  2025-01-01        M001       A        10
2  2025-01-02        M002       B        20
3  2025-01-02        M002       C        30
4  2025-01-03        M003       D        15

2025-11-29 17:30:01 - INFO - 開始移除重複記錄...
2025-11-29 17:30:01 - INFO - 檢查重複的依據欄位：['Date', 'Machine No.']
2025-11-29 17:30:01 - INFO - 保留策略：first
2025-11-29 17:30:01 - INFO - 移除了 150 筆重複記錄 (10.00%)
2025-11-29 17:30:01 - INFO - 清理後剩餘 1,350 筆記錄

清理後資料前 5 筆預覽：
         Date Machine No. Product  Quantity
0  2025-01-01        M001       A        10
1  2025-01-02        M002       B        20
2  2025-01-02        M002       C        30
3  2025-01-03        M003       D        15
4  2025-01-04        M004       E        25

2025-11-29 17:30:01 - INFO - 開始儲存清理後的資料...
2025-11-29 17:30:02 - INFO - 資料已成功儲存至：/Users/user/data/output.xlsx
2025-11-29 17:30:02 - INFO - 檔案大小：0.15 MB
2025-11-29 17:30:02 - INFO - ======================================================================
2025-11-29 17:30:02 - INFO - 資料清洗程式執行完成！
2025-11-29 17:30:02 - INFO - ======================================================================
```

### DEBUG 層級輸出

額外包含：
```
2025-11-29 17:30:01 - DEBUG - 資料框記憶體使用：0.25 MB
2025-11-29 17:30:01 - DEBUG - 欄位驗證通過：['Date', 'Machine No.']
```

## 錯誤處理

### 檔案不存在

**錯誤:**
```
2025-11-29 17:30:00 - ERROR - 檔案錯誤：找不到檔案：/path/to/nonexistent.xlsx
2025-11-29 17:30:00 - ERROR - 請確認檔案路徑是否正確
```

**解決方法:**
- 檢查檔案路徑是否正確
- 確認檔案確實存在
- 使用絕對路徑或相對路徑

### 欄位不存在

**錯誤:**
```
2025-11-29 17:30:01 - ERROR - 數值錯誤：資料中缺少以下必要欄位：['NonExistentColumn']
2025-11-29 17:30:01 - ERROR - 可用的欄位有：['Date', 'Machine No.', 'Product']
2025-11-29 17:30:01 - ERROR - 請檢查欄位名稱或參數設定
```

**解決方法:**
- 使用 `--log-level DEBUG` 查看可用欄位
- 確認欄位名稱拼寫正確（區分大小寫）
- 檢查欄位名稱中的空格

### 權限錯誤

**錯誤:**
```
2025-11-29 17:30:02 - ERROR - 權限錯誤：沒有檔案寫入權限
2025-11-29 17:30:02 - ERROR - 請確認有足夠的檔案讀寫權限
```

**解決方法:**
- 檢查輸出目錄的寫入權限
- 確認檔案未被其他程式開啟
- 嘗試使用不同的輸出路徑

## 提示與技巧

### 1. 先測試小樣本
```bash
# 使用 DEBUG 模式先測試
python "Data Clean.py" -i data.xlsx -o test.xlsx --log-level DEBUG
```

### 2. 檢查可用欄位
```bash
# 使用 DEBUG 層級查看所有欄位
python "Data Clean.py" -i data.xlsx -o test.xlsx --log-level DEBUG 2>&1 | grep "資料欄位"
```

### 3. 建立別名（macOS/Linux）
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中
alias dataclean='python "/path/to/Data Clean.py"'

# 使用
dataclean -i input.xlsx -o output.xlsx
```

### 4. 建立批次處理腳本
```bash
#!/bin/bash
# clean_all.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLEAN_SCRIPT="$SCRIPT_DIR/Data Clean.py"

for file in "$1"/*.xlsx; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .xlsx)
        echo "處理: $filename"
        python "$CLEAN_SCRIPT" \
            -i "$file" \
            -o "$2/${filename}_clean.xlsx" \
            --no-preview
    fi
done

echo "批次處理完成！"
```

**使用:**
```bash
chmod +x clean_all.sh
./clean_all.sh input_folder output_folder
```

## 常見問題

**Q: 如何知道有哪些欄位可用？**

A: 執行一次程式，它會在日誌中顯示所有欄位名稱，或使用 DEBUG 層級。

**Q: 欄位名稱有空格怎麼辦？**

A: 使用引號包圍：`-c "Machine No." "Product ID"`

**Q: 如何處理中文檔名？**

A: 直接使用引號包圍：`-i "我的資料.xlsx" -o "清理後.xlsx"`

**Q: 程式執行太慢怎麼辦？**

A: 使用 `--no-preview` 關閉資料預覽。

**Q: 如何自動化執行？**

A: 撰寫 shell 腳本或使用 cron job（Linux/macOS）或任務排程器（Windows）。

## 相關連結

- 專案 README: [README.md](README.md)
- 模組化版本: [src/main.py](src/main.py)
- 測試檔案: [tests/](tests/)

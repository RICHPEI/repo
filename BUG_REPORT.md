# Data Clean.py - Bug 分析報告

## 🔴 嚴重問題 (Critical)

### 1. 輸入輸出檔案相同時會覆蓋原始資料
**位置**: 第 403-404 行

**問題描述**:
沒有檢查輸入和輸出檔案是否相同，如果使用者指定相同的檔案，原始資料會被覆蓋。

```python
input_path = Path(args.input)
output_path = Path(args.output)
# 沒有檢查 input_path == output_path
```

**影響**:
- 可能導致資料永久遺失
- 沒有備份機制

**建議修復**:
```python
input_path = Path(args.input).resolve()
output_path = Path(args.output).resolve()

if input_path == output_path:
    logging.error("錯誤：輸入和輸出檔案不能相同")
    return 1
```

### 2. 日誌檔案目錄不存在時會失敗
**位置**: 第 40 行

**問題描述**:
如果指定的日誌檔案路徑包含不存在的目錄，FileHandler 會拋出異常。

```python
if log_file:
    handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    # 如果 log_file 是 "/non/existent/dir/app.log" 會失敗
```

**影響**:
- 程式無法啟動
- 錯誤訊息不清楚

**建議修復**:
```python
if log_file:
    # 確保日誌目錄存在
    log_file.parent.mkdir(parents=True, exist_ok=True)
    handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
```

### 3. 不支援舊版 Excel 檔案 (.xls)
**位置**: 第 106 行

**問題描述**:
硬編碼使用 openpyxl 引擎，不支援 .xls 格式。

```python
data_frame = pd.read_excel(file_path, engine='openpyxl')
# .xls 檔案會失敗
```

**影響**:
- 無法處理舊版 Excel 檔案
- 錯誤訊息可能令人困惑

**建議修復**:
```python
# 根據副檔名選擇引擎
if file_path.suffix.lower() == '.xls':
    data_frame = pd.read_excel(file_path, engine='xlrd')
elif file_path.suffix.lower() in ['.xlsx', '.xlsm']:
    data_frame = pd.read_excel(file_path, engine='openpyxl')
else:
    raise ValueError(f"不支援的檔案格式：{file_path.suffix}")
```

## 🟡 中等問題 (Medium)

### 4. 資料預覽使用 print() 而非 logging
**位置**: 第 417, 431 行

**問題描述**:
使用 print() 輸出資料預覽，不會記錄到日誌檔案。

```python
if not args.no_preview:
    logging.info("\n原始資料前 5 筆預覽：")
    print(original_data.head())  # 不會進入日誌檔案
```

**影響**:
- 日誌檔案不完整
- 難以追蹤實際處理的資料

**建議修復**:
```python
if not args.no_preview:
    logging.info("\n原始資料前 5 筆預覽：")
    logging.info(f"\n{original_data.head()}")
```

### 5. 沒有檔案覆蓋警告
**位置**: 第 435 行

**問題描述**:
如果輸出檔案已存在，會直接覆蓋，沒有警告。

```python
save_excel_data(cleaned_data, output_path, args.include_index)
# 不會警告檔案已存在
```

**建議修復**:
```python
if output_path.exists():
    logging.warning(f"警告：輸出檔案已存在，將被覆蓋：{output_path}")
```

### 6. 空欄位列表的特殊行為未說明
**位置**: 第 195-198 行

**問題描述**:
如果 duplicate_check_columns 為空列表，pandas 會檢查所有欄位，但這可能不是預期行為。

```python
cleaned_data_frame = data_frame.drop_duplicates(
    subset=duplicate_check_columns,  # 空列表會檢查所有欄位
    keep=keep_strategy,
    ignore_index=True
)
```

**建議修復**:
```python
if not duplicate_check_columns:
    logging.warning("警告：未指定檢查欄位，將檢查所有欄位")
```

### 7. 缺少檔案格式驗證
**位置**: 第 403-404 行

**問題描述**:
沒有驗證檔案副檔名是否為 Excel 格式。

**建議修復**:
```python
# 驗證輸入檔案格式
valid_extensions = {'.xlsx', '.xls', '.xlsm'}
if input_path.suffix.lower() not in valid_extensions:
    logging.error(f"不支援的檔案格式：{input_path.suffix}")
    logging.error(f"支援的格式：{', '.join(valid_extensions)}")
    return 1
```

### 8. 沒有處理磁碟空間不足
**位置**: 第 242-246 行

**問題描述**:
save_excel_data 只捕捉 PermissionError，沒有處理 OSError (磁碟滿)。

```python
except PermissionError as e:
    logging.error(f"沒有檔案寫入權限：{e}")
    raise
except Exception as e:  # 太廣泛
    logging.error(f"儲存檔案時發生錯誤：{e}")
    raise
```

**建議修復**:
```python
except PermissionError as e:
    logging.error(f"沒有檔案寫入權限：{e}")
    raise
except OSError as e:
    logging.error(f"儲存檔案失敗（可能是磁碟空間不足）：{e}")
    raise
except Exception as e:
    logging.error(f"儲存檔案時發生未預期錯誤：{e}")
    raise
```

## 🟢 輕微問題 (Minor)

### 9. setup_logging 的 log_level 驗證不足
**位置**: 第 43 行

**問題描述**:
如果 setup_logging() 被程式碼直接呼叫（非透過 CLI），無效的 log_level 會導致 AttributeError。

```python
level=getattr(logging, log_level.upper())
# 如果 log_level="INVALID" 會失敗
```

**建議修復**:
```python
try:
    level = getattr(logging, log_level.upper())
except AttributeError:
    logging.warning(f"無效的日誌層級：{log_level}，使用預設 INFO")
    level = logging.INFO
```

### 10. 檔案大小計算可能在部分寫入時不準確
**位置**: 第 248 行

**問題描述**:
假設檔案寫入成功，但在某些情況下可能有部分寫入。

```python
file_size = output_file_path.stat().st_size / 1024**2
# 如果寫入被中斷，檔案大小可能不正確
```

**建議修復**:
```python
if output_file_path.exists():
    file_size = output_file_path.stat().st_size / 1024**2
    logging.info(f"檔案大小：{file_size:.2f} MB")
else:
    logging.warning("警告：無法取得檔案大小資訊")
```

### 11. 類型忽略註解使用
**位置**: 第 421 行

**問題描述**:
使用 `# type: ignore` 來忽略類型錯誤，這不是最佳實踐。

```python
keep_strategy: Literal['first', 'last', False] = False if args.keep == 'none' else args.keep  # type: ignore
```

**建議修復**:
```python
from typing import Union

def remove_duplicate_records(
    data_frame: pd.DataFrame,
    duplicate_check_columns: List[str],
    keep_strategy: Union[Literal['first', 'last'], bool] = 'first'
) -> pd.DataFrame:
```

### 12. 沒有記憶體使用限制
**位置**: 第 106 行

**問題描述**:
沒有檢查檔案大小或記憶體限制，大檔案可能導致記憶體不足。

**建議修復**:
```python
# 在讀取前檢查檔案大小
file_size_mb = file_path.stat().st_size / 1024**2
if file_size_mb > 500:  # 500 MB 警告
    logging.warning(f"警告：檔案很大 ({file_size_mb:.2f} MB)，處理時間可能較長")
```

### 13. 缺少進度指示器
**位置**: 整個處理流程

**問題描述**:
大型檔案處理時沒有進度指示，使用者不知道程式是否仍在執行。

**建議改進**:
```python
# 可以使用 tqdm 或定期日誌輸出
from tqdm import tqdm
# 或在處理大型資料時定期輸出進度
```

## 📋 邊界情況 (Edge Cases)

### 14. 只有表頭沒有資料的 Excel
**問題**: 第 109 行的檢查會通過，但這可能不是期望的行為。

**建議**:
```python
if data_frame.empty:
    raise ValueError("讀取的資料框為空，無資料可處理")
if len(data_frame) == 0:
    raise ValueError("Excel 檔案只有表頭，沒有資料記錄")
```

### 15. 重複的欄位名稱
**問題**: Excel 可能有重複的欄位名稱（如 "Name", "Name.1"），驗證時可能出現問題。

**建議**:
```python
# 檢查是否有重複欄位名稱
if len(data_frame.columns) != len(set(data_frame.columns)):
    duplicate_cols = [col for col in data_frame.columns
                     if list(data_frame.columns).count(col) > 1]
    logging.warning(f"警告：資料中有重複的欄位名稱：{set(duplicate_cols)}")
```

### 16. 所有記錄都是重複的
**問題**: 如果使用 `keep='none'` 且所有記錄都重複，結果會是空資料框。

**建議**:
```python
if len(cleaned_data_frame) == 0:
    logging.warning("警告：清理後沒有剩餘記錄，所有資料都是重複的")
```

### 17. 欄位名稱包含特殊字元
**問題**: 欄位名稱可能包含空格、特殊字元，可能導致比對問題。

**建議**: 在文件中說明欄位名稱需要完全匹配，包括大小寫和空格。

## 🔒 安全性問題

### 18. 路徑遍歷攻擊
**問題**: 沒有驗證輸入路徑，可能受到路徑遍歷攻擊。

**建議**:
```python
# 使用 resolve() 獲取絕對路徑並驗證
input_path = Path(args.input).resolve()
# 可選：檢查路徑是否在允許的目錄內
```

### 19. 命令注入（透過檔名）
**問題**: 雖然不直接執行命令，但檔名可能包含特殊字元。

**建議**: 在文件中說明不建議使用特殊字元作為檔名。

## 📊 總結

| 嚴重程度 | 數量 | 優先處理 |
|---------|------|---------|
| 🔴 嚴重 | 3 | 是 |
| 🟡 中等 | 5 | 建議 |
| 🟢 輕微 | 5 | 可選 |
| 📋 邊界 | 4 | 文件化 |
| 🔒 安全 | 2 | 建議 |

**建議優先修復順序**:
1. 輸入輸出檔案相同檢查 (#1)
2. 日誌檔案目錄檢查 (#2)
3. 支援舊版 Excel (#3)
4. 檔案覆蓋警告 (#5)
5. 改用 logging 輸出預覽 (#4)

## 🛠️ 改進建議

1. **新增單元測試**: 測試所有邊界情況
2. **新增整合測試**: 測試完整工作流程
3. **改進錯誤訊息**: 提供更具體的解決建議
4. **新增配置檔支援**: 允許預設設定
5. **新增乾式執行模式**: `--dry-run` 只顯示會做什麼
6. **新增備份功能**: 自動備份原始檔案

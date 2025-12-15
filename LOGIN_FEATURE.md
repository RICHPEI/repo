# 使用者登入功能說明

這個文檔說明如何運行和使用新增的使用者登入功能。

## 功能特色

✅ React + TypeScript 前端介面
✅ Tailwind CSS 美觀樣式
✅ JWT Token 認證
✅ 記住我功能（localStorage / sessionStorage）
✅ 完整的錯誤處理
✅ FastAPI 後端 API

## 專案結構

```
/Users/richpei/myproject/Code/Python/Cursor/
├── frontend/                      # React 前端專案
│   ├── src/
│   │   ├── components/
│   │   │   └── LoginForm.tsx     # 登入表單組件
│   │   ├── services/
│   │   │   └── auth.ts           # 認證服務（JWT、localStorage）
│   │   ├── App.tsx               # 主應用程式
│   │   └── index.css             # Tailwind CSS
│   ├── vite.config.ts            # Vite 配置（包含 API 代理）
│   └── package.json
├── api/
│   ├── __init__.py
│   └── main.py                   # FastAPI 後端 API
├── requirements-api.txt          # Python API 依賴
└── src/                          # 原有的 Python Excel 工具
```

## 安裝依賴

### 1. 安裝 Python 後端依賴

```bash
pip install -r requirements-api.txt
```

### 2. 安裝前端依賴

```bash
cd frontend
npm install
```

## 運行應用程式

需要同時運行前端和後端服務器。

### 方法 1: 使用兩個終端視窗

**終端 1 - 運行後端 API:**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

**終端 2 - 運行前端開發服務器:**
```bash
cd frontend
npm run dev
```

然後在瀏覽器中開啟 http://localhost:5173

### 方法 2: 使用背景執行

```bash
# 在背景運行後端
python -m uvicorn api.main:app --reload --port 8000 &

# 運行前端
cd frontend && npm run dev
```

## 測試帳號

目前提供兩個測試帳號（在 `api/main.py` 的 `MOCK_USERS` 中定義）：

| Email | 密碼 | 名稱 |
|-------|------|------|
| test@example.com | password123 | 測試用戶 |
| admin@example.com | admin123 | 管理員 |

## API 端點

### POST /api/auth/login

**請求:**
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**成功回應 (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "1",
    "email": "test@example.com",
    "name": "測試用戶"
  }
}
```

**失敗回應 (401):**
```json
{
  "detail": "電子郵件或密碼錯誤"
}
```

### GET /api/health

健康檢查端點，返回服務器狀態。

## 功能說明

### 1. JWT Token 驗證

- Token 有效期限：30 分鐘
- Token 儲存在 `localStorage` 或 `sessionStorage`
- 自動驗證 token 格式和過期時間

### 2. 記住我功能

- ✅ 勾選「記住我」：使用 `localStorage`（持久化，關閉瀏覽器後仍保留）
- ❌ 未勾選「記住我」：使用 `sessionStorage`（關閉瀏覽器後清除）

### 3. 錯誤處理

- 網路連線錯誤
- 認證失敗（錯誤的帳號或密碼）
- Token 過期自動登出
- 表單驗證（email 格式檢查）

## 開發工具

### API 文檔

FastAPI 自動生成的互動式 API 文檔：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 前端開發

```bash
# 開發模式（熱重載）
npm run dev

# 建置生產版本
npm run build

# 預覽生產版本
npm run preview

# TypeScript 類型檢查
npm run typecheck
```

## 安全性注意事項

⚠️ **這是開發/演示版本，不適合直接用於生產環境！**

需要改進的安全性問題：

1. **SECRET_KEY**: 在 `api/main.py` 中使用環境變數而非硬編碼
2. **密碼加密**: 使用 bcrypt 或 Argon2 加密密碼，不要明文儲存
3. **HTTPS**: 生產環境必須使用 HTTPS
4. **CORS**: 限制允許的來源網域
5. **資料庫**: 使用真實資料庫（PostgreSQL、MySQL）而非模擬資料
6. **Token 刷新**: 實作 refresh token 機制
7. **速率限制**: 防止暴力破解攻擊

## 疑難排解

### 問題: 前端無法連接到後端

確認：
1. 後端服務器運行在 port 8000
2. Vite 代理配置正確 (`frontend/vite.config.ts`)
3. 檢查瀏覽器控制台的網路請求

### 問題: CORS 錯誤

確認：
1. `api/main.py` 中的 CORS 設定包含前端網址
2. 前端運行在 http://localhost:5173

### 問題: Token 驗證失敗

1. 檢查 token 是否過期（30 分鐘）
2. 清除瀏覽器的 localStorage 和 sessionStorage
3. 重新登入獲取新 token

## 下一步

- [ ] 整合真實資料庫
- [ ] 實作使用者註冊功能
- [ ] 添加密碼重設功能
- [ ] 實作角色權限管理
- [ ] 添加 E2E 測試
- [ ] 部署到生產環境

## 授權

MIT License

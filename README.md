## 專案結構簡介

```
2025DBMS-main/
├── backend/
│   ├── .env.example              # 範例環境變數設定檔
│   ├── requirements.txt          # Python 相依套件
│   └── db/
│       └── connection.py         # 資料庫連線設定
```

## 使用資料庫

本專案使用 **PostgreSQL** 作為主要資料庫。

### 步驟一：建立本地或連線遠端資料庫

請確認本機或遠端 PostgreSQL 伺服器已安裝並啟動。

1. **若需在本地建立一個新資料庫（例如 `dbms2025`）**

```bash
createdb dbms2025
```

建立資料庫後，請依序執行以下 SQL 檔案來初始化 schema 與預設資料，或使用任何 GUI 工具（如 pgAdmin）創建。

```bash
psql -d dbms2025 -f backend/db/init.sql
psql -d dbms2025 -f backend/db/insert_data.sql
```

請參考 `backend/.env.example` 複製為 `backend/.env`，並填入正確的連線資訊，範例格式如下。

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/dbms2025
```

2. **直接連線遠端資料庫**

本專案使用 Supabase（基於 PostgreSQL 的雲端平台）作為遠端資料庫。

請參考 `backend/.env.example` 複製為 `backend/.env`，並填入正確的連線資訊。

```
DATABASE_URL=<supabase_connection_string>
```

---

### 步驟二：安裝相依套件

請在 `backend` 資料夾內安裝所需 Python 套件：

```bash
cd backend
pip install -r requirements.txt
```

註：Windows 系統若想要建立虛擬環境可執行以下

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### 步驟三：確認可連線資料庫

請執行以下指令，確認資料庫連線成功：

```bash
python backend/db/connection.py
```

如果顯示成功連線與目前 timestamp，以及一筆 `listings` 資料表的資料，即表示資料庫連線成功。

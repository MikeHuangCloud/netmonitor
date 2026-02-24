# Network Monitor

簡易網路監控系統，透過 Ping 監測多個 IP 的網路狀態，並以圖表呈現歷史數據。

## 功能特色

- 🔐 管理員認證系統
- 🎯 多目標 IP 監控管理
- 📊 即時儀表板總覽
- 📈 延遲趨勢圖表 (Chart.js)
- 📉 成功率統計
- ⏰ 自動定時 Ping
- 🐳 Docker 容器化部署

## 技術棧

- **後端**: Python + Flask
- **資料庫**: MySQL 8.0
- **ORM**: SQLAlchemy
- **前端**: Bootstrap 5 + Chart.js
- **容器**: Docker + Docker Compose

## 快速開始

### 使用 Docker Compose (推薦)

```bash
# 1. 啟動服務
docker-compose up -d

# 2. 查看日誌
docker-compose logs -f

# 3. 停止服務
docker-compose down
```

### 本機開發

```bash
# 1. 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定環境變數
cp .env.example .env
# 編輯 .env 設定 MySQL 連接資訊

# 4. 啟動應用
python run.py
```

## 存取應用

- **網址**: http://localhost:5000
- **預設帳號**: admin
- **預設密碼**: admin123

> ⚠️ 請在正式環境中修改預設密碼！

## 環境變數

| 變數名稱 | 說明 | 預設值 |
|---------|------|--------|
| SECRET_KEY | Flask 密鑰 | dev-secret-key |
| MYSQL_HOST | MySQL 主機 | mysql |
| MYSQL_PORT | MySQL 端口 | 3306 |
| MYSQL_USER | MySQL 用戶 | netmonitor |
| MYSQL_PASSWORD | MySQL 密碼 | netmonitor123 |
| MYSQL_DATABASE | MySQL 資料庫 | netmonitor |
| PING_INTERVAL_SECONDS | Ping 間隔 | 60 |
| PING_COUNT | Ping 次數 | 4 |
| PING_TIMEOUT | Ping 超時 | 2 |
| DEFAULT_ADMIN_USERNAME | 預設管理員帳號 | admin |
| DEFAULT_ADMIN_PASSWORD | 預設管理員密碼 | admin123 |

## 專案結構

```
netmonitor/
├── config/             # 配置模組
├── models/             # Model 層 - 資料模型
├── views/              # View 層 - 頁面模板
├── controllers/        # Controller 層 - 路由控制
├── services/           # Service 層 - 業務邏輯
├── app.py              # Flask 應用工廠
├── run.py              # 啟動入口
├── scheduler.py        # 定時任務
├── Dockerfile          # Docker 映像配置
└── docker-compose.yml  # Docker Compose 配置
```

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | /api/stats | 取得儀表板統計 |
| GET | /api/chart-data | 取得圖表數據 |
| GET | /api/targets/:id/history | 取得目標歷史 |
| POST | /api/ping/execute | 手動執行 Ping |
| POST | /api/targets/:id/ping | 單一目標 Ping |

## License

MIT License

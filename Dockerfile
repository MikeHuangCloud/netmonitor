FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝 ping 工具
RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案並安裝（繞過 SSL 驗證）
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 複製應用程式碼
COPY . .

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

# 暴露端口
EXPOSE 5000

# 啟動應用
CMD ["python", "run.py"]

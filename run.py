import atexit
from app import create_app
from scheduler import init_scheduler, shutdown_scheduler

# 建立應用
app = create_app()

# 初始化排程器
init_scheduler(app)

# 註冊關閉時的清理函數
atexit.register(shutdown_scheduler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

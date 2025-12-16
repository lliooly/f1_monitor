from flask import Flask, render_template, jsonify, request
from datetime import datetime
from collections import deque
import threading
import time

# 导入核心模块
from config_manager import ConfigManager
from monitor_core import TicketMonitor

app = Flask(__name__)


class AppState:
    def __init__(self):
        self.logs = deque(maxlen=50)
        self.cards = {}
        self.monitor = None
        self.config = ConfigManager.load_config()


state = AppState()


# === 回调函数 ===
def web_log_callback(text):
    time_str = datetime.now().strftime("%H:%M:%S")
    state.logs.appendleft(f"[{time_str}] {text}")


def web_ui_callback(data):
    state.cards = data


# === 核心控制 ===
def start_monitor():
    """启动监控线程"""
    if state.monitor and state.monitor.is_running:
        return  # 已经在运行

    # 重新加载配置（确保读取到最新的）
    state.config = ConfigManager.load_config()
    if not state.config:
        web_log_callback("❌ 无法启动: 配置文件损坏或丢失")
        return

    state.monitor = TicketMonitor(
        config_data=state.config,
        log_callback=web_log_callback,
        update_ui_callback=web_ui_callback
    )
    state.monitor.start()
    web_log_callback("✅ 监控服务已启动")


def stop_monitor():
    """停止监控线程"""
    if state.monitor and state.monitor.is_running:
        state.monitor.stop()
        web_log_callback("⏹ 监控服务已停止")


# 初始化时自动启动
start_monitor()


# === Web 路由 ===

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    is_running = state.monitor.is_running if state.monitor else False
    return jsonify({
        "running": is_running,
        "logs": list(state.logs),
        "cards": state.cards
    })


@app.route('/api/control', methods=['POST'])
def control():
    action = request.json.get('action')
    if action == 'start':
        start_monitor()
    elif action == 'stop':
        stop_monitor()
    return jsonify({"status": "ok"})


# --- 新增：获取当前配置 ---
@app.route('/api/config', methods=['GET'])
def get_config_api():
    # 重新从磁盘加载，确保是最新的
    cfg = ConfigManager.load_config()
    return jsonify(cfg)


# --- 新增：保存配置 ---
@app.route('/api/config', methods=['POST'])
def save_config_api():
    data = request.json

    try:
        # 1. 保存到磁盘
        ConfigManager.save_config(
            cookie=data.get('cookie', ''),
            tg_token=data.get('tg_token', ''),
            tg_chat_id=data.get('tg_chat_id', ''),
            tg_master_switch=data.get('tg_master_switch', True),
            notification_rules=data.get('notification_rules', {}),
            refresh_interval=data.get('refresh_interval', 3)
        )

        # 2. 热重载：如果当前正在运行，需要重启以应用新配置
        was_running = state.monitor.is_running if state.monitor else False

        if was_running:
            stop_monitor()
            # 稍微等一下让线程完全退出
            time.sleep(0.5)
            start_monitor()
        else:
            # 如果没运行，只需刷新内存里的配置
            state.config = ConfigManager.load_config()

        web_log_callback("⚙️ 配置已保存并应用")
        return jsonify({"status": "ok", "msg": "配置保存成功"})

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
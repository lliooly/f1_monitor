import requests
import time
import threading


class TGBot:
    @staticmethod
    def send_message(token, chat_id, text):
        """
        发送单条消息，用于测试或普通通知
        返回: (bool, str) -> (是否成功, 错误信息/响应内容)
        """
        if not token or not chat_id:
            return False, "Token 或 Chat ID 为空"

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}

        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                return True, "发送成功"
            else:
                return False, f"发送失败 (HTTP {resp.status_code}): {resp.text}"
        except Exception as e:
            return False, f"网络错误: {str(e)}"

    @staticmethod
    def send_alert_sequence(token, chat_id, text, repeat_count=3):
        """
        启动一个线程发送报警序列（防阻塞主线程）
        """

        def _run():
            for i in range(repeat_count):
                success, msg = TGBot.send_message(token, chat_id, text)
                if not success:
                    print(f"报警发送失败 ({i + 1}/{repeat_count}): {msg}")
                time.sleep(1)  # 避免触发 TG 频率限制

        # 另起线程发送，不卡住监控逻辑
        threading.Thread(target=_run, daemon=True).start()
import requests
import time
import threading
import random
from tg_bot import TGBot


class TicketMonitor:
    def __init__(self, config_data, log_callback, update_ui_callback):
        self.config = config_data
        self.log = log_callback
        self.update_ui = update_ui_callback
        self.is_running = False
        self.last_notification_time = 0
        self.headers = self.config["headers_template"].copy()
        self.headers["Cookie"] = self.config["cookie"]

    def start(self):
        if self.is_running: return
        self.is_running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.is_running = False

    def _loop(self):
        interval = self.config['refresh_interval']
        tasks = self.config.get("tasks", [])
        self.log(f">>> 引擎启动: 监控中... (间隔 {interval}s)")

        while self.is_running:
            should_continue = self._scan_all_tasks(tasks)
            if not should_continue:
                self.stop()
                break

            jitter = random.uniform(-0.5, 0.5)
            time.sleep(max(1, interval + jitter))
        self.log(">>> 监控已停止")

    def _scan_all_tasks(self, tasks):
        all_counts = {}
        found_tickets_for_alert = []

        rules = self.config.get("notification_rules", {})

        for task in tasks:
            for name in task["targets"].values():
                all_counts[name] = 0

        for task in tasks:
            if not self.is_running: return True
            url = f"https://ztwen.jussyun.com/cyy_gatewayapi/show/pub/v3/show/{task['show_id']}/show_session/{task['session_id']}/seat_plans_dynamic_data?lang=en"

            try:
                time.sleep(0.2)
                resp = requests.get(url, headers=self.headers, timeout=5)
                if resp.status_code == 401 or "login" in resp.text.lower():
                    self._handle_cookie_expiry()
                    return False

                data = resp.json()
                if data.get("statusCode") != 200: continue

                dynamic_plans = data.get("data", {}).get("seatPlans", [])
                targets = task["targets"]

                for plan in dynamic_plans:
                    pid = plan.get("seatPlanId")
                    count = plan.get("canBuyCount", 0)

                    if pid in targets:
                        zone_name = targets[pid]
                        all_counts[zone_name] = count

                        if count > 0:
                            master_on = self.config.get("tg_master_switch", True)
                            item_on = rules.get(zone_name, True)

                            if master_on and item_on:
                                found_tickets_for_alert.append(f"✅ {zone_name}: {count}张")

            except:
                pass

        if not self.is_running: return True
        self.update_ui(all_counts)

        if found_tickets_for_alert:
            self.log(f"!!! 触发报警: {found_tickets_for_alert}")
            self._trigger_alert(found_tickets_for_alert)
        else:
            has_ticket = any(v > 0 for v in all_counts.values())
            status = "发现余票(已屏蔽通知)" if has_ticket else "暂无余票"
            self.log(f"扫描完成: {status}")

        return True

    def _handle_cookie_expiry(self):
        msg = "⚠️ Cookie 已过期！监控自动停止。"
        self.log(msg)
        if self.config.get("tg_master_switch", True):
            token = self.config.get("tg_token")
            chat_id = self.config.get("tg_chat_id")
            if token and chat_id:
                TGBot.send_message(token, chat_id, f"🚨 {msg}")

    def _trigger_alert(self, ticket_list):
        if time.time() - self.last_notification_time > 60:
            msg_body = "\n".join(ticket_list)
            full_msg = f"🚨 F1 监控报警 🚨\n{msg_body}\n\n立即去抢票！"

            token = self.config.get("tg_token")
            chat_id = self.config.get("tg_chat_id")
            if token and chat_id:
                TGBot.send_alert_sequence(token, chat_id, full_msg)

            self.last_notification_time = time.time()
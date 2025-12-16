import json
import os

CONFIG_FILE = "config.json"

# ==========================================
# F1 2026 全量票务数据库 (28组任务)
# ==========================================
DEFAULT_TASKS = [
    # --- 1. A 铂金 ---
    {
        "name": "A铂金-三日",
        "show_id": "6931340104da960001241d03",
        "session_id": "693134024996310001245614",
        "targets": {"693134024996310001245615": "A铂金-三日"}
    },

    # --- 2. A 看台 (包含上下层，分三日/周五/周六/周日) ---
    {
        "name": "A看台-三日",
        "show_id": "693133c84996310001244e59",
        "session_id": "693133c904da960001241609",
        "targets": {
            "693133c904da96000124160a": "A上-三日",
            "693782754996310001641319": "A下-三日"
        }
    },
    {
        "name": "A看台-周五",
        "show_id": "693133c84996310001244e59",
        "session_id": "693133c904da9600012415de",
        "targets": {
            "693133c904da9600012415e0": "A上-周五",
            "693133c904da9600012415e1": "A下-周五"
        }
    },
    {
        "name": "A看台-周六",
        "show_id": "693133c84996310001244e59",
        "session_id": "693133c904da9600012415f4",
        "targets": {
            "693133c904da9600012415f6": "A上-周六",
            "693133c904da9600012415f7": "A下-周六"
        }
    },
    {
        "name": "A看台-周日",
        "show_id": "693133c84996310001244e59",
        "session_id": "693133c904da9600012415bd",
        "targets": {
            "693133c904da9600012415be": "A上-周日",
            "693133c904da9600012415bf": "A下-周日"
        }
    },

    # --- 3. B 看台 ---
    {
        "name": "B看台-三日",
        "show_id": "693132f64996310001244995",
        "session_id": "693132f74996310001244a25",
        "targets": {"693132f74996310001244a26": "B看台-三日"}
    },
    {
        "name": "B看台-周五",
        "show_id": "693132f64996310001244995",
        "session_id": "693132f749963100012449d9",
        "targets": {"693132f749963100012449da": "B看台-周五"}
    },
    {
        "name": "B看台-周六",
        "show_id": "693132f64996310001244995",
        "session_id": "693132f74996310001244a13",
        "targets": {"693132f74996310001244a14": "B看台-周六"}
    },
    {
        "name": "B看台-周日",
        "show_id": "693132f64996310001244995",
        "session_id": "693132f749963100012449fe",
        "targets": {"693132f74996310001244a00": "B看台-周日"}
    },

    # --- 4. H 看台 ---
    {
        "name": "H看台-三日",
        "show_id": "6931529204da960001255be6",
        "session_id": "69315294499631000125956e",
        "targets": {"693152944996310001259573": "H看台-三日"}
    },
    {
        "name": "H看台-周五",
        "show_id": "6931529204da960001255be6",
        "session_id": "69315294499631000125957e",
        "targets": {"69315294499631000125957f": "H看台-周五"}
    },
    {
        "name": "H看台-周六",
        "show_id": "6931529204da960001255be6",
        "session_id": "693152944996310001259557",
        "targets": {"693152944996310001259558": "H看台-周六"}
    },
    {
        "name": "H看台-周日",
        "show_id": "6931529204da960001255be6",
        "session_id": "693152944996310001259593",
        "targets": {"693152944996310001259594": "H看台-周日"}
    },

    # --- 5. K 看台 ---
    {
        "name": "K看台-三日",
        "show_id": "693152ad04da960001255d56",
        "session_id": "693152ae04da960001255dd3",
        "targets": {"693152ae04da960001255dd9": "K看台-三日"}
    },
    {
        "name": "K看台-周五",
        "show_id": "693152ad04da960001255d56",
        "session_id": "693152ae04da960001255de9",
        "targets": {"693152ae04da960001255df1": "K看台-周五"}
    },
    {
        "name": "K看台-周六",
        "show_id": "693152ad04da960001255d56",
        "session_id": "693152ae04da960001255d91",
        "targets": {"693152ae04da960001255d9d": "K看台-周六"}
    },
    {
        "name": "K看台-周日",
        "show_id": "693152ad04da960001255d56",
        "session_id": "693152ae04da960001255db8",
        "targets": {"693152ae04da960001255dbd": "K看台-周日"}
    },

    # --- 6. E 看台 (仅三日) ---
    {
        "name": "E看台-三日",
        "show_id": "693152c604da960001255ee5",
        "session_id": "693152c74996310001259825",
        "targets": {"693152c74996310001259827": "E看台-三日"}
    },

    # --- 7. 草地 (C/F/J) ---
    {
        "name": "草地-三日",
        "show_id": "693153534996310001259a9f",
        "session_id": "6931535304da960001256187",
        "targets": {
            "6931535304da96000125618a": "草地C-三日",
            "6931535304da96000125618b": "草地F-三日",
            "6931535304da96000125618c": "草地J-三日"
        }
    },

    # --- 8. 围场俱乐部 ---
    {
        "name": "围场-三日",
        "show_id": "6933958049963100013a5c39",
        "session_id": "6933958104da9600013a271a",
        "targets": {"6933958104da9600013a271b": "Paddock Club"}
    },

    # --- 9. T1 Club (一号弯俱乐部) ---
    {
        "name": "T1 Club-三日",
        "show_id": "6937d3ce499631000168f5c0",
        "session_id": "6937d3cf04da96000168c4cd",
        "targets": {"6937d3cf04da96000168c4ce": "T1 Club-三日"}
    },
    {
        "name": "T1 Club-周五",
        "show_id": "6937d3ce499631000168f5c0",
        "session_id": "6937d3cf04da96000168c4a5",
        "targets": {"6937d3cf04da96000168c4a6": "T1 Club-周五"}
    },
    {
        "name": "T1 Club-周六",
        "show_id": "6937d3ce499631000168f5c0",
        "session_id": "6937d3cf04da96000168c4ed",
        "targets": {"6937d3cf04da96000168c4f1": "T1 Club-周六"}
    },
    {
        "name": "T1 Club-周日",
        "show_id": "6937d3ce499631000168f5c0",
        "session_id": "6937d3ce04da96000168c487",
        "targets": {"6937d3cf04da96000168c489": "T1 Club-周日"}
    },

    # --- 10. T16 Club (巅峰区/冲刺俱乐部) ---
    {
        "name": "T16 Club-三日",
        "show_id": "6932f40a04da9600013549e6",
        "session_id": "6932f40a499631000135817d",
        "targets": {"6932f40a499631000135817e": "T16巅峰-三日"}
    },
    {
        "name": "T16 Club-周五",
        "show_id": "6932f40a04da9600013549e6",
        "session_id": "6932f40b49963100013581b1",
        "targets": {"6932f40b49963100013581b4": "T16冲刺-周五"}
    },
    {
        "name": "T16 Club-周六",
        "show_id": "6932f40a04da9600013549e6",
        "session_id": "6932f40a4996310001358168",
        "targets": {"6932f40a4996310001358169": "T16冲刺-周六"}
    },
    {
        "name": "T16 Club-周日",
        "show_id": "6932f40a04da9600013549e6",
        "session_id": "6932f40a4996310001358195",
        "targets": {"6932f40a4996310001358197": "T16冲刺-周日"}
    }
]

DEFAULT_CONFIG = {
    "cookie": "",
    "tg_token": "",
    "tg_chat_id": "",
    "tg_switch": False,
    "notification_rules": {},
    "refresh_interval": 3,
    "tasks": DEFAULT_TASKS,
    "headers_template": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
        "Referer": "https://ztwen.jussyun.com/pc/content/693153534996310001259a9f",
        "terminal-src": "WEB",
        "product": "pc",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua-platform": "Windows",
        "lang": "en"
    }
}


class ConfigManager:
    @staticmethod
    def load_config():
        """加载配置"""
        if not os.path.exists(CONFIG_FILE):
            return None
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                if "tasks" not in data:
                    data["tasks"] = DEFAULT_TASKS

                # 初始化默认字段
                if "tg_master_switch" not in data:
                    data["tg_master_switch"] = True
                if "notification_rules" not in data:
                    data["notification_rules"] = {}

                return data
        except Exception:
            return None

    @staticmethod
    def save_config(cookie, tg_token, tg_chat_id, tg_master_switch, notification_rules, refresh_interval=3):
        """保存配置 (新增 rules 参数)"""
        current_data = DEFAULT_CONFIG.copy()

        # 尝试保留旧数据
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                    if "tasks" in existing and len(existing["tasks"]) > 0:
                        current_data["tasks"] = existing["tasks"]
                    else:
                        current_data["tasks"] = DEFAULT_TASKS
            except:
                pass
        else:
            current_data["tasks"] = DEFAULT_TASKS

        current_data["cookie"] = cookie.strip()
        current_data["tg_token"] = tg_token.strip()
        current_data["tg_chat_id"] = tg_chat_id.strip()
        current_data["tg_master_switch"] = bool(tg_master_switch)
        current_data["notification_rules"] = notification_rules
        current_data["refresh_interval"] = int(refresh_interval)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current_data, f, indent=4, ensure_ascii=False)

        return current_data
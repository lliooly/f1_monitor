import json
import os
from copy import deepcopy

CONFIG_FILE = "config.json"
ENV_FILE = ".env"
ENV_KEY_MAP = {
    "F1_MONITOR_COOKIE": "cookie",
    "F1_MONITOR_TG_TOKEN": "tg_token",
    "F1_MONITOR_TG_CHAT_ID": "tg_chat_id",
    "F1_MONITOR_TG_MASTER_SWITCH": "tg_master_switch",
    "F1_MONITOR_REFRESH_INTERVAL": "refresh_interval",
}

DEFAULT_TASKS = [
    {
        "name": "A铂金-三日",
        "show_id": "6931340104da960001241d03",
        "session_id": "693134024996310001245614",
        "targets": {"693134024996310001245615": "A铂金-三日"}
    },
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
    {
        "name": "E看台-三日",
        "show_id": "693152c604da960001255ee5",
        "session_id": "693152c74996310001259825",
        "targets": {"693152c74996310001259827": "E看台-三日"}
    },
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
    {
        "name": "围场-三日",
        "show_id": "6933958049963100013a5c39",
        "session_id": "6933958104da9600013a271a",
        "targets": {"6933958104da9600013a271b": "Paddock Club"}
    },
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
    "tg_master_switch": True,
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
    def _read_dotenv():
        values = {}
        if not os.path.exists(ENV_FILE):
            return values

        try:
            with open(ENV_FILE, "r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key:
                        values[key] = value
        except Exception:
            return {}

        return values

    @staticmethod
    def _parse_bool(value):
        return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}

    @staticmethod
    def _with_defaults(data):
        config = deepcopy(DEFAULT_CONFIG)
        config.update(data or {})

        if not config.get("tasks"):
            config["tasks"] = deepcopy(DEFAULT_TASKS)
        if "notification_rules" not in config or config["notification_rules"] is None:
            config["notification_rules"] = {}
        if "headers_template" not in config:
            config["headers_template"] = deepcopy(DEFAULT_CONFIG["headers_template"])
        if "tg_master_switch" not in config:
            config["tg_master_switch"] = True

        return config

    @staticmethod
    def _env_overrides(dotenv_values):
        overrides = {}
        for env_key, config_key in ENV_KEY_MAP.items():
            value = os.environ.get(env_key)
            if value is None:
                value = dotenv_values.get(env_key)
            if value in (None, ""):
                continue

            if config_key == "tg_master_switch":
                overrides[config_key] = ConfigManager._parse_bool(value)
            elif config_key == "refresh_interval":
                try:
                    overrides[config_key] = int(value)
                except ValueError:
                    pass
            else:
                overrides[config_key] = value

        return overrides

    @staticmethod
    def load_config():
        """加载配置"""
        dotenv_values = ConfigManager._read_dotenv()
        env_overrides = ConfigManager._env_overrides(dotenv_values)

        if not os.path.exists(CONFIG_FILE):
            if env_overrides:
                return ConfigManager._with_defaults(env_overrides)
            return None

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                config = ConfigManager._with_defaults(data)
                config.update(env_overrides)
                return config
        except Exception:
            return None

    @staticmethod
    def save_config(cookie, tg_token, tg_chat_id, tg_master_switch, notification_rules, refresh_interval=3):
        current_data = deepcopy(DEFAULT_CONFIG)

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
            current_data["tasks"] = deepcopy(DEFAULT_TASKS)

        current_data["cookie"] = cookie.strip()
        current_data["tg_token"] = tg_token.strip()
        current_data["tg_chat_id"] = tg_chat_id.strip()
        current_data["tg_master_switch"] = bool(tg_master_switch)
        current_data["notification_rules"] = notification_rules
        current_data["refresh_interval"] = int(refresh_interval)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current_data, f, indent=4, ensure_ascii=False)

        return current_data

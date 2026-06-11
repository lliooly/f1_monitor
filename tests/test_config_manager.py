import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config_manager import ConfigManager


ENV_KEYS = {
    "F1_MONITOR_COOKIE",
    "F1_MONITOR_TG_TOKEN",
    "F1_MONITOR_TG_CHAT_ID",
    "F1_MONITOR_TG_MASTER_SWITCH",
    "F1_MONITOR_REFRESH_INTERVAL",
}


class ConfigManagerEnvTest(unittest.TestCase):
    def test_load_config_uses_dotenv_when_config_file_is_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {key: "" for key in ENV_KEYS}, clear=False):
                for key in ENV_KEYS:
                    os.environ.pop(key, None)

                old_cwd = os.getcwd()
                try:
                    os.chdir(tmpdir)
                    Path(".env").write_text(
                        "\n".join(
                            [
                                "F1_MONITOR_COOKIE=dotenv-cookie",
                                "F1_MONITOR_TG_TOKEN=dotenv-token",
                                "F1_MONITOR_TG_CHAT_ID=123456",
                                "F1_MONITOR_TG_MASTER_SWITCH=false",
                                "F1_MONITOR_REFRESH_INTERVAL=9",
                            ]
                        ),
                        encoding="utf-8",
                    )

                    config = ConfigManager.load_config()
                finally:
                    os.chdir(old_cwd)

        self.assertEqual(config["cookie"], "dotenv-cookie")
        self.assertEqual(config["tg_token"], "dotenv-token")
        self.assertEqual(config["tg_chat_id"], "123456")
        self.assertFalse(config["tg_master_switch"])
        self.assertEqual(config["refresh_interval"], 9)
        self.assertGreater(len(config["tasks"]), 0)

    def test_environment_variables_override_config_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "F1_MONITOR_COOKIE": "env-cookie",
                    "F1_MONITOR_TG_TOKEN": "env-token",
                    "F1_MONITOR_TG_CHAT_ID": "654321",
                },
                clear=False,
            ):
                old_cwd = os.getcwd()
                try:
                    os.chdir(tmpdir)
                    Path("config.json").write_text(
                        json.dumps(
                            {
                                "cookie": "",
                                "tg_token": "",
                                "tg_chat_id": "",
                                "refresh_interval": 3,
                            }
                        ),
                        encoding="utf-8",
                    )

                    config = ConfigManager.load_config()
                finally:
                    os.chdir(old_cwd)

        self.assertEqual(config["cookie"], "env-cookie")
        self.assertEqual(config["tg_token"], "env-token")
        self.assertEqual(config["tg_chat_id"], "654321")
        self.assertEqual(config["refresh_interval"], 3)


if __name__ == "__main__":
    unittest.main()

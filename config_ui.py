import customtkinter as ctk
from tkinter import messagebox
from config_manager import ConfigManager, DEFAULT_CONFIG
from tg_bot import TGBot

class ConfigWindow(ctk.CTk):
    def __init__(self, on_save_callback):
        super().__init__()
        self.on_save = on_save_callback

        self.title("系统配置中心")
        self.geometry("550x700")
        ctk.set_appearance_mode("Dark")

        self.existing_config = ConfigManager.load_config() or DEFAULT_CONFIG

        self.all_zone_names = []
        if "tasks" in self.existing_config:
            for task in self.existing_config["tasks"]:
                self.all_zone_names.extend(task["targets"].values())
        self.all_zone_names = sorted(list(set(self.all_zone_names)))

        self.rules = self.existing_config.get("notification_rules", {})

        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, text="系统偏好设置", font=("Microsoft YaHei UI", 20, "bold")).pack(pady=15)

        self.tab_view = ctk.CTkTabview(self, width=500, height=550)
        self.tab_view.pack(pady=10, padx=20)

        self.tab_basic = self.tab_view.add("基础设置")
        self.tab_notify = self.tab_view.add("通知设置")


        ctk.CTkLabel(self.tab_basic, text="用户 Cookie (必填):", anchor="w").pack(fill="x", padx=10, pady=(15, 0))
        self.entry_cookie = ctk.CTkTextbox(self.tab_basic, height=120, border_width=2)
        self.entry_cookie.pack(fill="x", padx=10, pady=5)
        self.entry_cookie.insert("0.0", self.existing_config.get("cookie", ""))

        ctk.CTkLabel(self.tab_basic, text="刷新间隔 (秒):", anchor="w").pack(fill="x", padx=10, pady=(15, 0))
        self.entry_interval = ctk.CTkEntry(self.tab_basic)
        self.entry_interval.pack(fill="x", padx=10, pady=5)
        self.entry_interval.insert(0, str(self.existing_config.get("refresh_interval", 3)))

        ctk.CTkLabel(self.tab_notify, text="Bot Token:", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_token = ctk.CTkEntry(self.tab_notify, width=300)
        self.entry_token.grid(row=0, column=1, padx=10, pady=5)
        self.entry_token.insert(0, self.existing_config.get("tg_token", ""))

        ctk.CTkLabel(self.tab_notify, text="Chat ID:", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_chatid = ctk.CTkEntry(self.tab_notify, width=300)
        self.entry_chatid.grid(row=1, column=1, padx=10, pady=5)
        self.entry_chatid.insert(0, self.existing_config.get("tg_chat_id", ""))

        self.btn_test = ctk.CTkButton(self.tab_notify, text="🔔 测试连接", command=self.run_test, width=100)
        self.btn_test.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        ctk.CTkFrame(self.tab_notify, height=2, fg_color="#444").grid(row=3, column=0, columnspan=2, sticky="ew",
                                                                      pady=15, padx=10)
        self.master_var = ctk.BooleanVar(value=self.existing_config.get("tg_master_switch", True))
        self.switch_master = ctk.CTkSwitch(self.tab_notify, text="启用消息推送 (总开关)", variable=self.master_var,
                                           font=("Microsoft YaHei UI", 14, "bold"))
        self.switch_master.grid(row=4, column=0, columnspan=2, padx=10, sticky="w")

        ctk.CTkLabel(self.tab_notify, text="👇 独立通知管理 (勾选即推送):", text_color="gray").grid(row=5, column=0,
                                                                                                   columnspan=2,
                                                                                                   padx=10,
                                                                                                   pady=(15, 5),
                                                                                                   sticky="w")

        self.scroll_rules = ctk.CTkScrollableFrame(self.tab_notify, height=250, width=450)
        self.scroll_rules.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.check_vars = {}

        for idx, zone in enumerate(self.all_zone_names):
            is_checked = self.rules.get(zone, True)

            var = ctk.BooleanVar(value=is_checked)
            self.check_vars[zone] = var

            chk = ctk.CTkCheckBox(self.scroll_rules, text=zone, variable=var)
            chk.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        self.btn_save = ctk.CTkButton(self, text="💾 保存配置并重启", command=self.save_and_close,
                                      height=45, fg_color="#2CC985", hover_color="#229A65",
                                      font=("Microsoft YaHei UI", 15, "bold"))
        self.btn_save.pack(pady=10, padx=20, fill="x", side="bottom")

    def run_test(self):
        token = self.entry_token.get().strip()
        chat_id = self.entry_chatid.get().strip()
        if not token or not chat_id:
            messagebox.showwarning("提示", "请先填写 Token 和 Chat ID")
            return
        TGBot.send_message(token, chat_id, "👋 测试成功！")

    def save_and_close(self):
        cookie = self.entry_cookie.get("0.0", "end").strip()
        token = self.entry_token.get().strip()
        chat_id = self.entry_chatid.get().strip()
        interval = self.entry_interval.get().strip()
        master_switch = self.master_var.get()

        new_rules = {}
        for zone, var in self.check_vars.items():
            new_rules[zone] = var.get()

        if not cookie:
            self.entry_cookie.configure(border_color="red")
            return

        config_data = ConfigManager.save_config(cookie, token, chat_id, master_switch, new_rules, interval)
        self.destroy()
        self.on_save(config_data)
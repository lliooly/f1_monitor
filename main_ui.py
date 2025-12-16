import customtkinter as ctk
from datetime import datetime
from monitor_core import TicketMonitor
from config_manager import SEAT_MAPPING


class F1MonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === 窗口设置 ===
        self.title("F1 票务监控 Pro")
        self.geometry("600x650")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # === 初始化逻辑核心 ===
        # 将 GUI 的更新方法传给逻辑层
        self.monitor = TicketMonitor(
            log_callback=self.append_log,
            update_ui_callback=self.update_cards
        )

        # === 界面布局 ===
        self.setup_ui()

    def setup_ui(self):
        # 1. 标题
        ctk.CTkLabel(self, text="🏎️ F1 Ticket Hunter", font=("Roboto Medium", 24)).pack(pady=20)

        # 2. TG 配置区
        frame_cfg = ctk.CTkFrame(self)
        frame_cfg.pack(pady=10, padx=20, fill="x")

        self.entry_token = ctk.CTkEntry(frame_cfg, placeholder_text="TG Bot Token")
        self.entry_token.pack(pady=5, padx=10, fill="x")
        self.entry_chatid = ctk.CTkEntry(frame_cfg, placeholder_text="TG Chat ID")
        self.entry_chatid.pack(pady=5, padx=10, fill="x")

        # 3. 状态卡片区 (根据 Config 自动生成)
        frame_status = ctk.CTkFrame(self, fg_color="transparent")
        frame_status.pack(pady=10, padx=10, fill="x")

        self.cards = {}  # 存储卡片对象引用

        # 根据 SEAT_MAPPING 的值（草地C, F, J）生成卡片
        # 这里用 set 去重，防止 Config 写重复
        zone_names = sorted(list(set(SEAT_MAPPING.values())))

        for zone in zone_names:
            card = ctk.CTkFrame(frame_status, border_width=2, border_color="#444")
            card.pack(side="left", expand=True, fill="both", padx=5)

            lbl_title = ctk.CTkLabel(card, text=zone, font=("Roboto", 16, "bold"))
            lbl_title.pack(pady=(10, 0))

            lbl_count = ctk.CTkLabel(card, text="--", font=("Roboto", 20))
            lbl_count.pack(pady=(5, 10))

            self.cards[zone] = {"frame": card, "label": lbl_count}

        # 4. 按钮区
        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack(pady=10)

        self.btn_start = ctk.CTkButton(frame_btn, text="开始监控", command=self.on_start, fg_color="#2CC985",
                                       hover_color="#229A65")
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = ctk.CTkButton(frame_btn, text="停止", command=self.on_stop, fg_color="#C92C2C",
                                      hover_color="#9A2222", state="disabled")
        self.btn_stop.pack(side="left", padx=10)

        # 5. 日志区
        self.textbox_log = ctk.CTkTextbox(self, height=200)
        self.textbox_log.pack(pady=10, padx=20, fill="both", expand=True)

    # === 事件处理 ===
    def on_start(self):
        # 获取 TG 配置传给逻辑层
        token = self.entry_token.get().strip()
        chat_id = self.entry_chatid.get().strip()
        self.monitor.set_tg_config(token, chat_id)

        # 启动
        self.monitor.start()

        # 切换按钮状态
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")

    def on_stop(self):
        self.monitor.stop()
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

    # === 回调函数 (由 monitor_core 调用) ===
    def append_log(self, text):
        """逻辑层调用此方法写日志"""
        time_str = datetime.now().strftime("%H:%M:%S")
        self.textbox_log.insert("end", f"[{time_str}] {text}\n")
        self.textbox_log.see("end")

    def update_cards(self, count_dict):
        """逻辑层调用此方法更新卡片颜色和数字"""
        # data 格式: {"草地 C": 0, "草地 F": 5}
        for zone, count in count_dict.items():
            if zone in self.cards:
                ui = self.cards[zone]
                ui["label"].configure(text=f"{count} 张")

                # 有票变绿，没票灰色
                if count > 0:
                    ui["frame"].configure(border_color="#00FF00")
                    ui["label"].configure(text_color="#00FF00")
                else:
                    ui["frame"].configure(border_color="#444")
                    ui["label"].configure(text_color="gray")
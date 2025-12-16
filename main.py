import customtkinter as ctk
from datetime import datetime
import os
import time
import math  # 用于计算网格行数

from config_manager import ConfigManager
from config_ui import ConfigWindow
from monitor_core import TicketMonitor


class MonitorWindow(ctk.CTk):
    def __init__(self, config_data, show_config_callback):
        super().__init__()
        self.config_data = config_data
        self.show_config_callback = show_config_callback

        self.title("F1 票务监控 Pro - 全景大屏版")
        self.geometry("1000x750")  # 加宽窗口以容纳5列
        ctk.set_appearance_mode("Dark")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.monitor = TicketMonitor(
            config_data=self.config_data,
            log_callback=self.append_log,
            update_ui_callback=self.update_cards
        )

        self.setup_ui()

    def setup_ui(self):
        # === 1. 顶部控制栏 ===
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(15, 5), fill="x", padx=20)

        # 标题
        ctk.CTkLabel(header_frame, text="🏎️ F1 Ticket Hunter", font=("Roboto Medium", 24)).pack(side="left")

        # 右侧按钮组
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.pack(side="right")

        self.btn_start = ctk.CTkButton(btn_frame, text="▶ 开始监控", width=100, command=self.on_start,
                                       fg_color="#2CC985", hover_color="#229A65")
        self.btn_start.pack(side="left", padx=5)

        self.btn_stop = ctk.CTkButton(btn_frame, text="⏹ 停止", width=80, command=self.on_stop, fg_color="#C92C2C",
                                      hover_color="#9A2222", state="disabled")
        self.btn_stop.pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="⚙ 设置", width=60, command=self.on_settings_click, fg_color="#3B8ED0",
                      hover_color="#36719F").pack(side="left", padx=5)

        # === 2. 选项卡视图 (核心改动) ===
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(pady=10, padx=20, fill="both", expand=True)

        # 创建两个标签页
        self.tab_monitor = self.tab_view.add("🔴 实时监控")
        self.tab_logs = self.tab_view.add("📝 运行日志")

        # === Tab 1: 监控面板 (网格布局) ===
        # 使用 ScrollableFrame 使得内容过多时可以滚动
        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_monitor, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)

        self.cards = {}

        # 提取并排序所有票名
        all_zone_names = []
        if "tasks" in self.config_data:
            for task in self.config_data["tasks"]:
                all_zone_names.extend(task["targets"].values())
        zone_names = sorted(list(set(all_zone_names)))

        # 配置网格列权重 (5列)
        for i in range(5):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

        # 动态生成卡片 (5个一行)
        for idx, zone in enumerate(zone_names):
            row = idx // 5  # 第几行
            col = idx % 5  # 第几列

            # 卡片容器
            card = ctk.CTkFrame(self.scroll_frame, border_width=2, border_color="#333", corner_radius=10)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")  # sticky="nsew" 让卡片填满格子

            # 区域名称 (上方)
            # 使用 text_wrap=True 防止名字太长显示不全
            ctk.CTkLabel(card, text=zone, font=("Microsoft YaHei UI", 13, "bold"), wraplength=140).pack(pady=(15, 5),
                                                                                                        padx=5)

            # 余票数字 (中间，大号字体)
            lbl_count = ctk.CTkLabel(card, text="--", font=("Roboto", 28, "bold"), text_color="gray")
            lbl_count.pack(pady=(0, 15))

            self.cards[zone] = {"frame": card, "label": lbl_count}

        # === Tab 2: 日志面板 ===
        self.textbox_log = ctk.CTkTextbox(self.tab_logs, font=("Consolas", 12))
        self.textbox_log.pack(fill="both", expand=True, padx=5, pady=5)
        self.append_log("系统就绪。点击顶部 [▶ 开始监控] 启动引擎。")

    # --- 逻辑控制 ---
    def on_start(self):
        self.monitor.start()
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.tab_view.set("🔴 实时监控")  # 自动切回监控页

    def on_stop(self):
        self.monitor.stop()
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")

    def on_close(self):
        try:
            self.monitor.stop()
            self.quit()
            self.destroy()
        except:
            pass

    def on_settings_click(self):
        self.on_stop()
        self.after(100, self._safe_switch_to_config)

    def _safe_switch_to_config(self):
        try:
            self.quit()
            self.destroy()
            self.show_config_callback()
        except:
            pass

    def append_log(self, text):
        try:
            if not self.winfo_exists(): return
            time_str = datetime.now().strftime("%H:%M:%S")
            self.textbox_log.insert("end", f"[{time_str}] {text}\n")
            self.textbox_log.see("end")
        except:
            pass

    def update_cards(self, count_dict):
        try:
            if not self.winfo_exists(): return

            for zone, count in count_dict.items():
                if zone in self.cards:
                    ui = self.cards[zone]
                    try:
                        ui["label"].configure(text=str(count))
                        if count > 0:
                            # 有票：亮绿色边框 + 亮绿色文字
                            ui["frame"].configure(border_color="#00FF00", border_width=3)
                            ui["label"].configure(text_color="#00FF00")
                        else:
                            # 无票：深灰色边框 + 灰色文字
                            ui["frame"].configure(border_color="#333", border_width=2)
                            ui["label"].configure(text_color="gray")
                    except:
                        pass
        except:
            pass


# --- 程序编排 ---

def launch_monitor(config_data):
    app = MonitorWindow(config_data, show_config_callback=launch_config)
    app.mainloop()


def launch_config():
    app = ConfigWindow(on_save_callback=launch_monitor)
    app.mainloop()


def main():
    config = ConfigManager.load_config()
    if config:
        launch_monitor(config)
    else:
        launch_config()


if __name__ == "__main__":
    main()
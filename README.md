# 🏎️ F1 Ticket Monitor (Desktop Edition)

F1 上海站票务监控工具

基于 Python + CustomTkinter 构建，提供现代化的界面，支持多区域实时监控与 Telegram 报警。

## ✨ 主要功能

* **全景监控**：支持 A/B/H/K/E/草地/包厢等全站 30+ 种票务的实时库存监控。
* **暗黑 UI**：基于 CustomTkinter 的现代化网格布局，5 列显示，清晰直观。
* **Telegram 报警**：发现余票立即推送到手机，支持“总开关”和“精细化单项开关”控制。
* **静默模式**：无本地铃声干扰，适合宿舍/办公室挂机。
* **可视化配置**：内置独立的配置面板，无需修改代码即可更新 Cookie 和通知规则。
* **防封策略**：随机化请求间隔 + 智能 Cookie 过期检测。

## 🛠️ 环境要求

* Python 3.10 或更高版本
* 依赖库：`requests`, `customtkinter`, `packaging`

## 🚀 快速开始

### 1. 安装依赖
在项目根目录下运行：
```bash
pip install requests customtkinter packaging
```

### 2. 启动程序
```bash
python main.py
```

### 3. 配置
一、默认配置
1. 程序启动后，点击右上角的 **“设置”** 按钮。
2. **Cookie (必填)**：使用 Fiddler 或浏览器 F12 抓取 `ztwen.jussyun.com` 的请求，复制 Cookie 填入。
3. **Telegram 通知 (选填)**：
* 填入 Bot Token 和 Chat ID。
* 勾选 **“启用消息推送 (总开关)”**。
* 在下方的列表中，**勾选**你希望收到通知的票种（例如：只勾选 "A铂金" 和 "草地C"，屏蔽其他 999999 的票）。
4. 点击 **“💾 保存并重启”**。

二、手动配置

打开 **config.json**手动配置以下三个内容：

    "cookie": "",
    "tg_token": "",
    "tg_chat_id": "",

## 📂 文件结构
* `main.py`: **入口文件**，负责 GUI 界面绘制和逻辑调度。
* `monitor_core.py`: **核心引擎**，负责多线程轮询 API 和数据清洗。
* `config_manager.py`: **配置管理**，负责读写 `config.json` 和管理票务任务列表。
* `config_ui.py`: **设置窗口**，独立的配置界面代码。
* `tg_bot.py`: **通知模块**，负责发送 Telegram 消息。

##⚠️ 注意事项* **Cookie 有效期**：久事体育的 Cookie 通常只有数小时有效期。如果日志提示“Cookie 已过期”，请重新抓包并更新。
* **刷新频率**：建议设置在 3 秒以上，过快可能导致 IP 被暂时封禁。

---

*Created by shishishi3*
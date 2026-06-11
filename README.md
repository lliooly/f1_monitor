# 🏎️ F1 Ticket Monitor (Docker Web Edition)

F1 上海站票务监控工具。

采用 Flask 后端 + HTML5 前端，适配 Docker 部署。支持手机/iPad 远程查看，配合 Nginx Proxy Manager 实现域名访问。

## ✨ 特性

* **Web 大屏**：响应式暗黑网页设计，手机、平板、电脑浏览器均可访问。
* **Docker 部署**：环境隔离，开箱即用，支持后台运行。
* **在线配置**：直接在网页端修改 Cookie、Telegram 开关和监控规则，自动热重启服务。
* **精细化通知**：支持对每一种票单独设置“是否推送 TG”。
* **日志回溯**：网页端保留最近 50 条运行日志，方便排查问题。

## 🔐 本地配置

推荐使用 `.env` 保存本地敏感配置：

```bash
cp .env.example .env
```

然后填写：

```dotenv
F1_MONITOR_COOKIE=
F1_MONITOR_TG_TOKEN=
F1_MONITOR_TG_CHAT_ID=
F1_MONITOR_TG_MASTER_SWITCH=true
F1_MONITOR_REFRESH_INTERVAL=3
```

也可以复制 `config.example.json` 为 `config.json` 后手动填写。`.env` 和 `config.json` 都是本地私有文件，已被 `.gitignore` 忽略，**不要提交真实 Cookie、Bot Token 或 Chat ID**。

环境变量优先级高于 `config.json`，适合 Docker、服务器部署和临时覆盖本地配置。

## 📦 部署指南 (Docker Compose)

### 方法一：独立部署

1. 确保已安装 Docker 和 Docker Compose。
2. 复制 `.env.example` 为 `.env`，或复制 `config.example.json` 为 `config.json`。
3. 运行启动命令：

```bash
docker-compose up -d --build
```

### 方法二：合并部署

如果你已有现成的 `docker-compose.yml`，可直接添加服务：

```yaml
  f1-monitor:
    build: ./f1_monitor_web
    image: f1-monitor:latest
    container_name: f1-monitor
    restart: unless-stopped
    ports:
      - "5050:5000"
    volumes:
      - ./f1_monitor_web/config.json:/app/config.json
    env_file:
      - ./f1_monitor_web/.env
    environment:
      - TZ=Asia/Shanghai
```

如果只使用 `.env`，可以不挂载 `config.json`。

## 🌐 访问与使用

1. 浏览器打开 `http://<服务器IP>:5050`，例如 `http://192.168.31.50:5050`。
2. 点击右上角的 **“⚙ 设置”**。
3. 填入抓包获取的 **Cookie**。
4. 配置 **Telegram** 相关信息。
5. 在下方复选框中勾选你想要报警的票种。
6. 点击保存，服务会自动重启监控线程。

## 🔧 常见问题

**Q: 镜像拉取失败 (timeout)?**

A: 由于网络环境问题，如果无法拉取基础镜像，可以在 Docker Desktop 的 Settings 中配置 registry mirror 后重试。

**Q: 如何更新代码?**

A: 修改本地 Python 代码后，需要重新构建容器生效：

```bash
docker-compose up -d --build
```

## 📂 目录结构

* `Dockerfile`: 镜像构建文件。
* `web_app.py`: Flask 后端，提供 API 和页面服务。
* `templates/index.html`: 前端监控大屏源码。
* `monitor_core.py`: 监控核心逻辑。
* `config_manager.py`: 配置管理，负责读取 `.env`、环境变量和本地 `config.json`。
* `.env.example`: 环境变量模板，复制为 `.env` 后填写本地敏感配置。
* `config.example.json`: JSON 配置模板，复制为 `config.json` 后填写本地敏感配置。

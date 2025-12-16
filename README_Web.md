# 🏎️ F1 Ticket Hunter (Docker Web Edition)

F1 上海站票务监控工具。

采用 Flask 后端 + HTML5 前端，完美适配 Docker 部署。支持手机/iPad 远程查看，配合 Nginx Proxy Manager 实现域名访问。

## ✨ 特性

* **Web 大屏**：响应式暗黑网页设计，手机、平板、电脑浏览器均可完美访问。
* **Docker 部署**：环境隔离，开箱即用，支持 7x24 小时后台运行。
* **在线配置**：直接在网页端修改 Cookie、Telegram 开关和监控规则，自动热重启服务。
* **精细化通知**：支持对每一种票单独设置“是否推送 TG”，告别垃圾消息轰炸。
* **日志回溯**：网页端保留最近 50 条运行日志，方便排查问题。

## 📦 部署指南 (Docker Compose)

### 方法一：独立部署

1.  确保已安装 Docker 和 Docker Compose。
2.  在项目根目录下创建 `config.json` (空文件即可，用于挂载)。
3.  运行启动命令：

```bash
# 构建镜像并后台启动
docker-compose up -d --build
```

###方法二：合并部署 (推荐)如果你已有现成的 `docker-compose.yml` (如包含 NPM, Portainer)，可直接添加服务：

```yaml
  f1-monitor:
    build: ./f1_monitor_web  # 指向代码目录
    image: f1-monitor:latest
    container_name: f1-monitor
    restart: unless-stopped
    ports:
      - "5050:5000"          # 外部端口 5050
    volumes:
      - ./f1_monitor_web/config.json:/app/config.json
    environment:
      - TZ=Asia/Shanghai
```

## 🌐 访问与使用
1. **访问地址**：
* 浏览器打开 `http://<服务器IP>:5050` (例如 `http://192.168.31.50:5050`)。


2. **初始化配置**：
* 点击右上角的 **“⚙ 设置”**。
* 填入抓包获取的 **Cookie**。
* 配置 **Telegram** 相关信息。
* 在下方的复选框中，**勾选**你想要报警的票种。
* 点击保存，服务会自动重启监控线程。


3. **外网访问 (可选)**：
* 配合 Nginx Proxy Manager，将域名 (如 `f1.example.com`) 反向代理到容器的 `5000` 端口 (或局域网 IP 的 `5050` 端口)。



## 🔧 常见问题
**Q: 镜像拉取失败 (timeout)?**

A: 由于网络环境问题，如果无法拉取 `python:3.13-slim`，建议使用离线导入方式：

1. 在能联网的机器下载镜像：`docker save -o python.tar python:3.13-slim`
2. 上传到服务器并导入：`docker load -i python.tar`
3. 修改 Dockerfile 使用导入的镜像 ID。

**Q: 如何更新代码?**

A: 修改本地 Python 代码后，需要重新构建容器生效：

```bash
docker-compose up -d --build
```

## 📂 目录结构* `Dockerfile`: 镜像构建文件。
* `web_app.py`: Flask 后端，提供 API 和页面服务。
* `templates/index.html`: 前端监控大屏源码。
* `monitor_core.py`: 监控核心逻辑 (复用)。
* `config.json`: 配置文件 (由 Docker 挂载持久化保存)。


---

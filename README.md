# LET MONITOR

一个基于 Workers AI 的 LowEndTalk 新帖/评论监控。获取到信息后，交由 AI 进行翻译、总结、筛选，并推送到 Telegram 等不同渠道。

DEMO：

## 功能

- **新帖监控**：监控 offer 区新帖，并由AI进行总结翻译。
- **评论监控**：监控帖子作者的后续评论，由AI筛选有价值评论推送。

## 限制

AI 需要调校，可能会输出预期以外的结果。

## 安装和配置

### Docker 安装

```
docker run -v ./vps-stock-monitor:/app/data -p 5000:5000 vpslog/vps-stock-monitor
```

访问`5000`端口进行设置即可。

如需配置代理或者启用密码验证，建议使用 `docker-compose` 安装

```bash
https://github.com/vpslog/vps-stock-monitor/
cd vps-stock-monitor
# nano docker-compose.yml 修改密码
docker compose up -d
```

访问`8080`即可

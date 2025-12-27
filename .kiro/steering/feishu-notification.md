---
inclusion: manual
---

# 飞书通知方法

当需要发送飞书通知时，参考以下方法。

## Webhook 方式

### 基本格式
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"消息内容"}}' \
  "https://open.feishu.cn/open-apis/bot/v2/hook/{WEBHOOK_ID}"
```

### 消息类型

#### 1. 纯文本
```json
{
  "msg_type": "text",
  "content": {
    "text": "这是一条文本消息"
  }
}
```

#### 2. 富文本（支持换行、@人）
```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "标题",
        "content": [
          [{"tag": "text", "text": "第一行"}],
          [{"tag": "text", "text": "第二行"}]
        ]
      }
    }
  }
}
```

#### 3. 卡片消息
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "标题"},
      "template": "blue"
    },
    "elements": [
      {"tag": "div", "text": {"tag": "plain_text", "content": "内容"}}
    ]
  }
}
```

## GitHub Actions 中使用

### 1. 添加 Secret
- 路径：`Settings > Secrets and variables > Actions > New repository secret`
- Name: `FEISHU_WEBHOOK`
- Value: 完整的 webhook URL

### 2. Workflow 示例
```yaml
- name: Send to Feishu
  env:
    FEISHU_WEBHOOK: ${{ secrets.FEISHU_WEBHOOK }}
  run: |
    MESSAGE="通知内容"
    curl -X POST \
      -H "Content-Type: application/json" \
      -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"$MESSAGE\"}}" \
      "$FEISHU_WEBHOOK"
```

### 3. 定时触发（cron）
```yaml
on:
  schedule:
    # 北京时间 8:00 = UTC 0:00
    - cron: '0 0 * * *'
```

## 现有实现

- `.github/workflows/daily-feishu-quote.yml` - 每日随机句子推送

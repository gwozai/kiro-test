# Kiro MCP Server 配置指南

本文档记录如何在 Kiro 中配置 GitHub MCP Server。

## 什么是 MCP Server？

MCP (Model Context Protocol) 是一种让 AI 工具直接连接外部服务的协议。GitHub MCP Server 让 AI 助手可以：

- 浏览和搜索仓库代码
- 创建和管理 Issues、Pull Requests
- 查看 GitHub Actions 工作流
- 分析代码安全问题
- 管理团队协作

## 配置步骤

### 1. 创建 GitHub Personal Access Token

访问 https://github.com/settings/tokens/new?type=classic

- Note: 填写 `kiro-mcp`
- Expiration: 选择有效期
- 勾选 `repo` 权限
- 点击 Generate token

### 2. 配置 Kiro

在项目根目录创建 `.kiro/settings/mcp.json`：

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN_HERE"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

将 `YOUR_TOKEN_HERE` 替换为你的 GitHub PAT。

### 3. 验证配置

在 Kiro 中测试：
- 询问 "获取我的 GitHub 用户信息"
- 如果返回你的用户名，说明配置成功

## 可用功能

| 功能 | 说明 |
|------|------|
| 用户信息 | 获取用户资料 |
| 仓库管理 | 创建、搜索、浏览仓库 |
| Issues | 创建、更新、搜索 issues |
| Pull Requests | 创建、合并、review PR |
| 代码搜索 | 跨仓库搜索代码 |
| 文件操作 | 创建、更新、删除文件 |

## 注意事项

⚠️ **安全提醒**：不要将包含真实 token 的配置文件提交到公开仓库！

建议将 `.kiro/settings/mcp.json` 添加到 `.gitignore`。

## 参考链接

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Kiro 文档](https://kiro.dev)

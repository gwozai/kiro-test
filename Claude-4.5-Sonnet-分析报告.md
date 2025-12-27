# Claude 4.5 Sonnet 系统提示词分析报告

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| 来源 | system_prompts_leaks/Anthropic/claude-4.5-sonnet.md |
| 模型 | Claude 4.5 Sonnet |
| 文件大小 | ~2700+ 行 |
| 分析日期 | 2025-12-27 |

---

## 🔍 整体架构

Claude 4.5 Sonnet 的系统提示词是一个**超大型、模块化**的指令集，与 GPT-5.1 的简洁风格形成鲜明对比。

### 主要模块

```
Claude 4.5 Sonnet 系统提示词
├── citation_instructions      # 引用规则
├── past_chats_tools          # 历史对话工具
├── computer_use              # 计算机使用能力
│   ├── skills                # 技能系统
│   ├── file_handling_rules   # 文件处理规则
│   ├── artifacts             # Artifact 创建
│   └── package_management    # 包管理
├── claude_completions_in_artifacts  # Artifact 中调用 Claude API
├── search_instructions       # 搜索指令（最复杂）
│   ├── query_complexity_categories  # 查询复杂度分类
│   ├── web_search_usage_guidelines  # 搜索使用指南
│   └── mandatory_copyright_requirements  # 版权要求
├── preferences_info          # 用户偏好处理
└── functions                 # 可用工具定义
```

---

## 🎯 核心设计理念

### 1. 引用系统（Citation System）

Claude 4.5 有一套精密的引用系统：

```xml
<cite index="DOC_INDEX-SENTENCE_INDEX">引用内容</cite>
```

**关键规则：**
- 每个来自搜索的声明都必须用 `<cite>` 标签包裹
- 支持单句、连续句、多段落引用
- **绝对禁止**直接引用原文，必须用自己的话重述

### 2. 历史对话工具（Past Chats Tools）

Claude 4.5 可以搜索用户的历史对话：

| 工具 | 用途 |
|------|------|
| `conversation_search` | 按主题/关键词搜索 |
| `recent_chats` | 按时间检索（1-20条） |

**触发模式识别：**
- 显式引用："继续我们关于...的对话"
- 时间引用："昨天我们聊了什么"
- 隐式信号：过去时态、所有格、定冠词

### 3. 计算机使用能力（Computer Use）

Claude 4.5 可以操作 Linux 计算机（Ubuntu 24）：

**可用工具：**
- `bash` - 执行命令
- `str_replace` - 编辑文件
- `file_create` - 创建文件
- `view` - 查看文件/目录

**文件系统规则：**
```
/mnt/user-data/uploads  → 用户上传的文件
/home/claude            → Claude 的工作目录
/mnt/user-data/outputs  → 最终输出（用户可见）
```

### 4. 技能系统（Skills）

Claude 4.5 有一套"技能"系统，每种文件类型都有最佳实践：

| 技能 | 位置 | 用途 |
|------|------|------|
| docx | /mnt/skills/public/docx/SKILL.md | Word 文档 |
| pdf | /mnt/skills/public/pdf/SKILL.md | PDF 文件 |
| pptx | /mnt/skills/public/pptx/SKILL.md | PPT 演示 |
| xlsx | /mnt/skills/public/xlsx/SKILL.md | Excel 表格 |

**强制要求**：在创建任何文档前，必须先读取对应的 SKILL.md 文件！

### 5. Artifact 系统

Claude 4.5 可以创建多种类型的 Artifact：

| 类型 | 扩展名 | 特殊渲染 |
|------|--------|----------|
| Markdown | .md | ✅ |
| HTML | .html | ✅ |
| React | .jsx | ✅ |
| Mermaid | .mermaid | ✅ |
| SVG | .svg | ✅ |
| PDF | .pdf | ✅ |

**React Artifact 可用库：**
- lucide-react, recharts, MathJS, lodash, d3, Plotly
- Three.js (r128), Chart.js, Tone, tensorflow
- shadcn/ui, Papaparse, SheetJS

**关键限制：**
> ⚠️ **绝对禁止**使用 localStorage、sessionStorage 等浏览器存储 API！

### 6. Claude-in-Claude（Claudeception）

Claude 4.5 可以在 Artifact 中调用 Claude API：

```javascript
const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1000,
    messages: [{ role: "user", content: "Your prompt here" }]
  })
});
```

**无需 API Key**，后端自动处理！

---

## 🔎 搜索系统深度分析

这是 Claude 4.5 最复杂的模块，占据了大量篇幅。

### 查询复杂度分类

| 类别 | 工具调用次数 | 示例 |
|------|-------------|------|
| **Never Search** | 0 | 基础知识、编程帮助、历史事实 |
| **Do Not Search But Offer** | 0（但提供搜索） | 年度统计数据 |
| **Single Search** | 1 | 当前天气、最新新闻、实时汇率 |
| **Research** | 2-20 | 复杂分析、报告、多源对比 |

### 搜索决策树

```
查询是否涉及稳定信息？
├── 是 → 直接回答，不搜索
└── 否 → 信息变化频率？
    ├── 每日/每周 → 立即搜索
    ├── 每年 → 先回答，提供搜索
    └── 不确定 → 检查是否有未知实体
        ├── 有 → 单次搜索
        └── 无 → 根据复杂度决定
```

### 版权保护规则

**绝对禁止：**
- 引用超过 30 个词的原文
- 复制歌词（任何形式）
- 创建"替代性摘要"（过于详细的总结）

**必须做到：**
- 用自己的话重述
- 提供引用标记
- 建议用户查看原文

---

## 📊 与 GPT-5.1 对比

| 维度 | GPT-5.1 Default | Claude 4.5 Sonnet |
|------|-----------------|-------------------|
| **提示词长度** | ~20 行 | ~2700+ 行 |
| **设计风格** | 极简、人格导向 | 详尽、功能导向 |
| **核心定位** | AI 教练 | 多功能助手 |
| **工具能力** | 未在提示词中定义 | 详细定义（计算机、搜索、文件） |
| **引用系统** | 无 | 精密的 XML 标签系统 |
| **版权保护** | 未提及 | 大量篇幅强调 |
| **用户偏好** | 未提及 | 详细的偏好处理规则 |

### 设计哲学差异

**GPT-5.1**：
> "告诉 AI 它是谁，让它自己决定怎么做"

**Claude 4.5**：
> "详细规定每种情况下应该怎么做"

---

## 💡 关键设计亮点

### 1. 模块化架构
每个功能都有独立的 XML 标签包裹，便于维护和更新。

### 2. 决策树设计
搜索系统使用清晰的决策树，减少 AI 的"判断负担"。

### 3. 示例驱动
大量使用 `<example>` 标签，通过示例教会 AI 正确行为。

### 4. 安全优先
版权保护、有害内容过滤都有专门的模块。

### 5. 技能系统
将最佳实践外置到 SKILL.md 文件，实现"知识与指令分离"。

---

## 🛠️ 实践启示

### 对提示词工程的借鉴

1. **模块化设计**
   - 大型提示词应该分模块
   - 每个模块用 XML 标签包裹
   - 便于维护和调试

2. **决策树模式**
   - 复杂决策用决策树表达
   - 减少 AI 的"自由发挥"空间
   - 提高行为一致性

3. **示例驱动**
   - 抽象规则 + 具体示例
   - 示例比规则更容易被 AI 理解
   - 包含正例和反例

4. **安全边界**
   - 明确禁止的行为
   - 版权、隐私、有害内容
   - 使用强调词（CRITICAL、NEVER）

5. **工具使用规范**
   - 详细定义每个工具的使用场景
   - 提供调用示例
   - 说明限制和边界

### 可复用的模式

```xml
<module_name>
  <overview>模块概述</overview>
  <rules>
    - 规则1
    - 规则2
  </rules>
  <examples>
    <example>
      <user>用户输入</user>
      <response>期望响应</response>
      <rationale>为什么这样响应</rationale>
    </example>
  </examples>
  <critical_notes>
    - 关键注意事项
  </critical_notes>
</module_name>
```

---

## 📝 总结

Claude 4.5 Sonnet 的系统提示词是一个**工业级**的指令集，体现了 Anthropic 对 AI 行为控制的深度思考：

1. **功能全面** - 搜索、文件、计算机、引用、偏好全覆盖
2. **规则详尽** - 每种情况都有明确的处理方式
3. **安全优先** - 版权、隐私、有害内容层层把关
4. **示例丰富** - 大量示例确保 AI 理解意图

与 GPT-5.1 的"人格导向"设计不同，Claude 4.5 采用"功能导向"设计，更像是一本详尽的操作手册。

**适用场景：**
- 需要精确控制 AI 行为的企业应用
- 涉及版权、隐私等敏感场景
- 需要多工具协作的复杂任务

---

*分析完成于 2025-12-27*

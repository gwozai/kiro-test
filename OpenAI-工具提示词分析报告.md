# OpenAI 工具提示词设计分析报告

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| 来源 | system_prompts_leaks/OpenAI/tool-*.md |
| 文件数量 | 9 个工具定义文件 |
| 类型 | 功能型（工具定义） |
| 分析日期 | 2025-12-27 |

---

## 🔍 工具清单

```
OpenAI 工具系统
├── 记忆系统
│   ├── tool-memory-bio.md          # 基础记忆（bio）
│   └── tool-advanced-memory.md     # 高级记忆（新版）
├── 代码执行
│   ├── tool-python.md              # Python 执行
│   └── tool-python-code.md         # Python 代码（同上）
├── 内容创作
│   ├── tool-canvas-canmore.md      # Canvas 画布
│   └── tool-create-image-image_gen.md  # 图像生成
├── 信息检索
│   ├── tool-web-search.md          # 网页搜索
│   ├── tool-file_search.md         # 文件搜索
│   └── tool-deep-research.md       # 深度研究
```

---

## 🎯 各工具详细分析

### 1. 记忆工具（bio / advanced-memory）

#### bio（基础记忆）
```
## bio
The bio tool allows you to persist information across conversations.
Address your message to=bio and write whatever information you want to remember.
```

**设计特点：**
- 极简设计，仅 3 行
- 使用 `to=bio` 的消息路由机制
- 信息会出现在未来对话的上下文中

#### advanced-memory（高级记忆）

**三大记忆模块：**

| 模块 | 内容 | 置信度 |
|------|------|--------|
| Assistant Response Preferences | 用户偏好（基于历史对话推断） | high |
| Notable Past Conversation Topics | 历史对话主题摘要 | high |
| Helpful User Insights | 用户洞察信息 | high |

**用户元数据收集：**
```
- 平均消息长度：5217.7 字符
- 地理位置（可能不准确，如使用 VPN）
- 设备信息（屏幕尺寸、像素比、浏览器）
- 模型使用分布：38% o3, 36% gpt-4o, 13% o4-mini...
- 账户年龄：126 周
- 订阅计划：ChatGPT Pro
- 对话质量分类：36% good, 33% bad
```

**隐藏工具（alpha_tools）：**
- `monologue_summary` - 长消息摘要
- `search_web_open` - 搜索+打开合一
- `browser`（已废弃）→ 被 `web` 替代
- `my_files_browser`（已废弃）→ 自动文件暴露

---

### 2. Python 执行工具

```
## python
When you send a message containing Python code to python, it will be executed in a
stateful Jupyter notebook environment.
```

**关键规则：**

| 规则 | 说明 |
|------|------|
| 执行环境 | 有状态的 Jupyter notebook |
| 超时时间 | 60 秒 |
| 文件存储 | `/mnt/data` 可持久化 |
| 网络访问 | **禁用** |
| DataFrame 展示 | `ace_tools.display_dataframe_to_user()` |

**图表规则（重复强调）：**
```
I REPEAT: when making charts for the user:
1) use matplotlib over seaborn        # 禁用 seaborn
2) give each chart its own distinct plot (no subplots)  # 禁止子图
3) never, ever, specify colors or matplotlib styles     # 禁止指定颜色
```

**设计洞察：** 通过 "I REPEAT" 强调关键规则，说明这是常见的违规点。

---

### 3. Canvas 画布工具（canmore）

**三个函数：**

| 函数 | 用途 | 触发条件 |
|------|------|----------|
| `create_textdoc` | 创建文档/代码 | 用户明确要迭代长文档或代码 |
| `update_textdoc` | 更新文档 | 文档已存在 |
| `comment_textdoc` | 添加评论 | 文档已存在 |

**文档类型：**
```javascript
type: "document" | "code/python" | "code/javascript" | "code/html" | "code/java" | "code/react" | ...
```

**React 代码规范：**
```
- Default export a React component
- Use Tailwind for styling, no import needed
- All NPM libraries are available
- Use shadcn/ui for basic components
- Use lucide-react for icons
- Use recharts for charts
- Use Framer Motion for animations
- 2xl rounded corners, soft shadows
- Grid-based layouts
```

**更新策略：**
```
ALWAYS REWRITE CODE TEXTDOCS USING A SINGLE UPDATE WITH ".*" FOR THE PATTERN
```
代码文件总是全量替换，不做局部更新。

---

### 4. 图像生成工具（image_gen）

**核心函数：**
```typescript
type text2im = (_: {
  prompt?: string,
  size?: string,
  n?: number,
  transparent_background?: boolean,
  referenced_image_ids?: string[],
}) => any;
```

**关键规则：**

| 规则 | 说明 |
|------|------|
| 直接生成 | 不需要确认，除非涉及用户本人 |
| 用户肖像 | **必须**至少询问一次是否上传照片 |
| 生成后 | 不提下载、不总结、不问后续问题 |
| 图像编辑 | 优先用 image_gen，不用 python |
| 违规处理 | 建议必须与原始违规"足够不同" |

**设计洞察：** 用户肖像的特殊处理体现了隐私保护意识。

---

### 5. 网页搜索工具（web）

**触发场景：**
```
- Local Information: 本地信息（天气、商家、活动）
- Freshness: 信息可能过时
- Niche Information: 小众/专业信息
- Accuracy: 错误代价高（软件版本、赛事日期）
```

**命令：**
```
- search(): 搜索引擎查询
- open_url(url: str): 打开指定 URL
```

**重要提示：**
```
IMPORTANT: Do not attempt to use the old `browser` tool or generate responses 
from the `browser` tool anymore, as it is now deprecated or disabled.
```

---

### 6. 文件搜索工具（file_search）

**最复杂的工具**，包含高级搜索语法：

**搜索操作符：**

| 操作符 | 用途 | 示例 |
|--------|------|------|
| `+` | 提升包含该词的文档 | `+GPT4`, `+(John Doe)` |
| `--QDF=` | 新鲜度要求（0-5） | `--QDF=5` 表示需要最新信息 |

**QDF（Query Deserved Freshness）等级：**

| 等级 | 含义 | 时间范围 |
|------|------|----------|
| 0 | 历史信息/不变事实 | 无限制 |
| 1 | 一般可接受 | 18 个月内 |
| 2 | 变化较慢 | 6 个月内 |
| 3 | 可能变化 | 3 个月内 |
| 4 | 较新信息 | 60 天内 |
| 5 | 最新信息 | 30 天内 |

**多语言支持：**
```
当用户问题不是英语时，必须同时发送英语和用户语言的查询
```

**示例：**
```json
// 韩语查询
User: 김민준이 무엇을 하고 있나요?
=> {"queries": [
  "current projects tasks for +(Kim Minjun) --QDF=3",
  "현재 프로젝트 및 작업 +(김민준) --QDF=3"
]}
```

**引用格式：**
```
msearch: 【{message idx}:{search idx}†{source}†{line range}】
mclick:  【{message idx}†{source}†{line range}】
```

---

### 7. 深度研究工具（deep-research）

**核心能力：**
- 使用 `research_kickoff_tool` 进行广泛在线研究
- 支持 `clarify_with_text` 和 `start_research_task`

**限制：**
```
- 只能访问公开信息
- 不能访问需要登录的网站
- Python 中禁止绑图表、安装包、保存图片
```

**输出格式要求：**
```markdown
- 主标题: #
- 子标题: ##, ###
- 段落: 3-5 句
- 列表: - 或 1.
```

**引用规则：**
```
必须保留 【{cursor}†L{line_start}(-L{line_end})?】 格式的引用
embed_image 引用必须放在段落开头，不能放在标题前
```

---

## 📊 设计模式总结

### 1. 消息路由机制
```
to=bio          → 记忆工具
to=file_search.msearch  → 文件搜索
to=file_search.mclick   → 文件点击
```

### 2. 命名空间设计
```typescript
namespace image_gen {
  type text2im = (...) => any;
}

namespace file_search {
  type msearch = (...) => any;
}
```

### 3. 规则强调模式
```
I REPEAT: ...
IMPORTANT: ...
ALWAYS: ...
NEVER: ...
```

### 4. 示例驱动
每个复杂工具都提供大量示例，如 file_search 的查询示例。

### 5. 废弃声明
```
(deprecated) - 明确标注已废弃的工具
```

---

## 💡 设计亮点

### 1. QDF 新鲜度系统
file_search 的 QDF 系统是一个精妙的设计：
- 0-5 的量化等级
- 每个等级对应明确的时间范围
- 让 AI 能够智能判断信息新鲜度需求

### 2. 多语言查询策略
```
非英语查询 → 同时发送英语 + 原语言查询
```
这确保了跨语言搜索的准确性。

### 3. 用户元数据收集
advanced-memory 收集的元数据非常详细：
- 使用模式（模型分布、对话深度）
- 设备信息（屏幕、浏览器）
- 行为分析（消息长度、活跃度）

### 4. 对话质量分类
```
460 messages are good interaction quality (36%)
420 messages are bad interaction quality (33%)
```
用于训练数据筛选。

### 5. 图表规则的重复强调
```
I REPEAT: when making charts...
```
说明这是常见的违规点，通过重复强调来强化规则。

---

## 🛠️ 实践启示

### 工具定义模板

```markdown
## tool_name

// 工具描述和使用场景
// - 场景1
// - 场景2

// 关键规则（使用 IMPORTANT/NEVER/ALWAYS 强调）

namespace tool_name {
  type function_name = (_: {
    param1?: type,
    param2?: type,
  }) => any;
}
```

### 搜索工具设计要点

1. **新鲜度控制** - 提供量化的新鲜度参数
2. **多语言支持** - 同时查询多种语言
3. **操作符设计** - 提供 `+`、`--QDF=` 等高级操作符
4. **引用格式** - 定义清晰的引用格式

### 代码执行工具设计要点

1. **环境说明** - 明确执行环境（Jupyter）
2. **超时设置** - 明确超时时间
3. **存储路径** - 指定文件存储位置
4. **网络限制** - 明确网络访问权限
5. **输出规范** - 提供专用的展示函数

### 内容创作工具设计要点

1. **触发条件** - 明确何时使用
2. **类型系统** - 定义支持的内容类型
3. **更新策略** - 全量替换 vs 局部更新
4. **样式规范** - 提供详细的样式指南

---

## 📝 总结

OpenAI 的工具提示词设计体现了以下特点：

1. **模块化** - 每个工具独立定义，职责清晰
2. **类型安全** - 使用 TypeScript 风格的类型定义
3. **规则明确** - 大量使用 IMPORTANT/NEVER/ALWAYS
4. **示例丰富** - 复杂工具提供详细示例
5. **版本管理** - 明确标注废弃工具
6. **隐私意识** - 用户肖像等敏感场景有特殊处理

这套工具系统是一个**工业级**的设计，值得在构建 AI Agent 时参考借鉴。

---

*分析完成于 2025-12-27*

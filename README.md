# SellerSprite Amazon Market Research BI Skill

## 从一个关键词和竞品 ASIN，找到真正相关的产品，并做成可审计的 Amazon 品类 BI

一个面向 Amazon 选品、市场研究和竞品分析的 Codex Skill。它把 SellerSprite（卖家精灵）的关键词、竞品、标准导出和详细导出连接成一条完整工作流：

**关键词扩展 -> 相似产品发现 -> Listing 属性筛选 -> 目标 ASIN 审计 -> 父 ASIN 去重 -> 交互式 BI Dashboard**

它解决的不是“把 Excel 画成图”，而是先回答一个更关键的问题：**哪些产品真的属于你要研究的市场？**

[在线体验 AI Voice Recorder BI Dashboard](https://pdben-auto.github.io/sellersprite-amazon-market-research-bi-skill/) · [查看完整 Skill](sellersprite-bi-market-research/SKILL.md) · [查看关键词与相关性方法](sellersprite-bi-market-research/references/discovery-and-relevance-workflow.md) · [查看案例方法](sellersprite-bi-market-research/references/worked-example-ai-voice-recorder.md)

## Live Demo：最终 BI 呈现效果

[打开 AI Voice Recorder Amazon US 交互式 BI](https://pdben-auto.github.io/sellersprite-amazon-market-research-bi-skill/) · [查看或下载单文件 HTML](docs/index.html)

Demo 是本次完整研究流程的实际输出，包含：

- 核心直接市场与传统录音笔相邻市场分层。
- 年度、YTD、同周期同比和月度趋势。
- 父 ASIN 去重后的品牌销售额竞争与市场集中度。
- 关键词证据、产品属性筛选、父体商品明细和排名动量。
- 数据来源、范围、计算口径、冲突和缺失说明。

这是基于指定关键词、竞品和详细导出构建的查询样本，不代表完整 `AI Voice Recorder` 类目 TAM。数据截止日为 `2026-09-21`，最后完整月份为 `2026-08`。Dashboard 为自包含静态 HTML，不需要 localhost 或后端服务。

## 它解决什么问题

常见的 Amazon 品类研究容易出现这些失真：

- 只搜一个大词，把附件、套装、替代品和关键词堆砌产品一起算进市场。
- 只看核心竞品，没有系统扩展长尾关键词和相似 ASIN。
- 标准导出有几百个商品，详细导出只有几十个，却把全部商品放进销量分母。
- 将父体下的多个子 ASIN 重复相加，夸大销量和销售额。
- 把关键词购买量、SellerSprite 销售额、模拟 GMV 和 Amazon BSR 混为一谈。
- 能做图表，但无法解释某个 ASIN 为什么被纳入或排除。

本 Skill 用候选清单、四层相关性判断和详细数据覆盖闸门，把“市场边界”变成可以检查、修改和复现的数据资产。

## 核心能力

- 从 `seed keyword + competitor ASIN` 扩展关键词和相似产品。
- 按搜索意图聚类：通用品类、AI 结果、使用场景、产品形态、商业约束、品牌词和噪声词。
- 汇总关键词高频 ASIN、竞品搜索结果、种子父子体和 Listing 相关产品。
- 从标题、类目和 Listing 属性中提取形态、容量、兼容设备、尺寸、重量、订阅、套装等筛选维度。
- 将候选分为 `core_direct`、`adjacent_substitute`、`excluded_noise`、`review`。
- 保留每个候选的来源、分数、判断原因、属性证据和详细导出覆盖状态。
- 以父 ASIN 为销售统计粒度，避免兄弟子体重复相加。
- 分开计算 SellerSprite 销售额、销量、价格和模拟 GMV。
- 输出年度、YTD、同周期同比、品牌销售额竞争和全局排名动量。
- 生成可直接打开、不依赖服务器或外部 CDN 的单文件交互式 HTML BI。

## 为什么值得使用

### 1. 先建立正确的市场，再计算市场

关键词结果只是发现样本，不自动等于完整品类 TAM。Skill 会显式区分：

- `Category Baseline`：经过单独验证的品类大盘。
- `Core Direct Market`：解决同一客户任务的直接竞争产品。
- `Adjacent/Substitute Market`：只解决部分任务或结构不同的替代产品。

### 2. 每一个纳入与排除都有证据

被排除的商品不会直接消失。`candidate_manifest.csv` 会保留 ASIN、来源、Listing 属性、决定和理由，方便团队复核高销售额排除项或规则误判。

### 3. 避免 SellerSprite 导出范围不一致造成的虚假份额

只有被目标市场接受、并且得到详细导出覆盖的 ASIN，才会进入销售额、销量、父体数量和份额分母。标准导出可以更宽，但不能偷偷扩大销售市场。

### 4. 案例规则不会污染其他品类

AI 录音设备案例中的品牌、订阅、转录和降噪规则只属于该项目。其他品类复用的是方法、证据结构和数据闸门，而不是 Plaud 或录音笔专属判断。

## 前提条件

### 必需条件

| 条件 | 用途 | 缺失时的行为 |
| --- | --- | --- |
| Codex 或兼容 Agent Skills 的运行环境 | 加载并执行 `SKILL.md` | 无法作为自动发现的 Skill 运行，但脚本仍可单独使用 |
| Python 3.10+ | 运行发现和规范化脚本 | 停止自动处理并报告依赖缺失 |
| `openpyxl` 3.x | 读取 SellerSprite XLSX 导出 | 停止 XLSX 处理，不伪造结果 |
| SellerSprite 关键词/竞品导出 | 从关键词和竞品发现候选 | 可从已有 ASIN 开始，但会标记关键词覆盖不完整 |
| SellerSprite 详细导出 | 年度、同比、销售额与历史趋势 | 降级为当前快照，不输出虚构历史 |
| 明确的站点、产品任务和市场边界 | 决定什么是核心、相邻和无关产品 | 停止市场容量结论，先输出待确认范围 |

### 条件必需或可选增强

- SellerSprite 授权账号和网络：只有需要在线重新采集时才必需。
- SellerSprite 标准导出：用于父子 ASIN、品牌、标题、图片、类目和 Listing 属性。
- Amazon Listing：用于处理标准导出无法解决的属性歧义。
- 浏览器或 Playwright：用于在线采集和最终 HTML 验证。
- Feishu MCP：只有用户明确要求写入飞书时才需要。

SellerSprite 数据属于第三方估算，不是 Amazon 结算数据。本项目不会保存 SellerSprite/Amazon 凭证，也不会把 Cookie、Token 或账号信息写入导出和 HTML。

## 实战案例：AI Voice Recorder

案例从下面两个输入开始：

```text
Seed keyword: ai voice recorder
Core competitor ASIN: B0FYQ4Y2ZZ
Marketplace: Amazon US
```

### 研究边界

- 核心客户任务：实体设备完成录音，并提供转录、总结、AI 笔记/文档或翻译结果。
- 直接竞品：同时满足录音和 AI 信息处理结果的专用便携设备。
- 相邻替代：主要把 `AI` 用于降噪、声控或音频清理的传统录音笔。
- 排除项：电脑搭售录音器、保护壳、充电器、无关电子产品、关键词堆砌商品，以及会扭曲单机经济性的多设备套装。

### 关键词意图

案例将关键词拆为：

- Generic category
- AI outcome
- Use case
- Form factor
- Commercial constraint
- Brand/product family
- Accessory/noise

### Listing 属性筛选

候选产品可以按以下属性复核或筛选：

- 卡片、磁吸、穿戴、胸针、口袋或录音笔形态
- 存储容量和兼容设备
- 转录、总结、笔记、文档和翻译能力
- 免费分钟数、订阅方案、离线能力和 App 依赖
- 尺寸、重量、包装数量和套装内容

### 关键数据规则

标准导出可能包含广泛候选，但只有详细导出覆盖的已接受 ASIN 才进入 BI 销售分母。详细表缺失的父 ASIN 会优先使用标准表的 child-to-parent 映射补齐；仍无法解析的记录明确标记，而不是猜测。

[阅读完整 AI Voice Recorder 方法和验收标准](sellersprite-bi-market-research/references/worked-example-ai-voice-recorder.md)

## 安装

### 方式一：Clone 后复制到 Codex Skills

```bash
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force `
  ".\sellersprite-amazon-market-research-bi-skill\sellersprite-bi-market-research" `
  "$env:USERPROFILE\.codex\skills\sellersprite-bi-market-research"
```

macOS/Linux：

```bash
cp -R ./sellersprite-amazon-market-research-bi-skill/sellersprite-bi-market-research \
  ~/.codex/skills/sellersprite-bi-market-research
```

安装 Python 依赖：

```bash
python -m pip install -r requirements.txt
```

### 方式二：直接下载仓库 ZIP

在 GitHub 页面选择 `Code -> Download ZIP`，解压后将 `sellersprite-bi-market-research` 文件夹复制到 Codex 的 skills 目录。

## 使用示例

安装后可以直接提出：

```text
使用 $sellersprite-bi-market-research。
站点是 Amazon US，种子关键词是 ai voice recorder，
核心竞品是 B0FYQ4Y2ZZ。
请扩展相关关键词和相似产品，按 Listing 的转录、总结、订阅、
产品形态和套装属性筛选目标 ASIN，再用 SellerSprite 标准/详细导出制作 BI。
```

其他触发示例：

```text
我给你一个关键词和竞品 ASIN，先找相关产品和关键词，筛掉无关 Listing，再做 SellerSprite BI。
```

```text
把这批 SellerSprite 标准/详细导出按父 ASIN 去重，制作年度、同比、品牌销售额和排名动量看板。
```

## 脚本快速使用

### 1. 发现关键词和候选 ASIN

```powershell
python sellersprite-bi-market-research/scripts/discover_sellersprite_market.py `
  --keyword-export "path/to/keyword-mining.xlsx" `
  --competitor-export "path/to/competitor-standard.xlsx" `
  --detail "path/to/selected-detail.xlsx" `
  --rules "path/to/discovery-rules.json" `
  --seed-keyword "ai voice recorder" `
  --seed-asin "B0FYQ4Y2ZZ" `
  --output-dir "path/to/discovery"
```

### 2. 规范化已筛选市场

```powershell
python sellersprite-bi-market-research/scripts/normalize_sellersprite_exports.py `
  --standard "path/to/standard.xlsx" `
  --detail "path/to/detail.xlsx" `
  --scope-manifest "path/to/candidate_manifest.csv" `
  --include-decisions "core_direct" `
  --output-dir "path/to/normalized" `
  --as-of 2026-09-21 `
  --market-name "AI voice recorder direct sample" `
  --marketplace "Amazon US"
```

## 主要输出

| 输出 | 用途 |
| --- | --- |
| `keyword_evidence.csv` | 关键词聚类、需求和竞争证据 |
| `candidate_manifest.csv` | 所有候选 ASIN、相关性决定、原因、属性和详细覆盖 |
| `parent_scope_manifest.csv` | 父 ASIN 去重后的市场范围 |
| `target_child_asins.txt` | 可提交 SellerSprite 详细导出的目标子 ASIN |
| `parent_monthly.csv` | 父 ASIN 月度销量、销售额和模拟 GMV |
| `market_monthly.csv` | 市场月度趋势及同比 |
| `parent_current.csv` | 最新完整月竞争明细 |
| `rank_momentum.csv` | 固定全局分母的排名动量，不是 Amazon BSR |
| `conflicts.csv` | 子体历史冲突和选值审计 |
| `dashboard.html` | 可通过 `file://` 直接打开的交互式 BI |

## 质量保证

- 候选范围、关键词、父子 ASIN、判断理由和数据覆盖可追溯。
- 真实的 0 与缺失值严格区分。
- 完整年、部分年、YTD 和同周期同比严格使用对应月份。
- 核心直接市场与相邻替代市场分别规范化和展示。
- 测试覆盖关键词聚类、候选分层、父体去重、销售额、排名动量、缺失销售额和范围过滤。
- Skill 通过 Codex `quick_validate.py` 结构校验。

运行测试：

```bash
python -m unittest discover -s sellersprite-bi-market-research/scripts -p "test_*.py" -v
```

## 项目结构

```text
.
|-- README.md
|-- requirements.txt
|-- docs/
|   `-- index.html
`-- sellersprite-bi-market-research/
    |-- SKILL.md
    |-- agents/openai.yaml
    |-- references/
    |   |-- collection-workflow.md
    |   |-- dashboard-standard.md
    |   |-- data-contract.md
    |   |-- discovery-and-relevance-workflow.md
    |   `-- worked-example-ai-voice-recorder.md
    |-- scripts/
    `-- tests/trigger-cases.md
```

## Search Keywords

SellerSprite, 卖家精灵, Amazon market research, Amazon product research, Amazon FBA, keyword research, ASIN research, competitor analysis, similar product discovery, Listing attribute filtering, parent ASIN deduplication, Amazon BI dashboard, e-commerce analytics, product opportunity analysis, AI voice recorder market, Codex skills, Agent Skills, 亚马逊选品, 亚马逊市场调研, 关键词挖掘, 竞品分析, ASIN 筛选, 父体去重, 品类 BI, 品牌销售额, 产品机会分析。

## Disclaimer

This project is not affiliated with SellerSprite or Amazon. SellerSprite estimates should be treated as third-party market evidence, not Amazon settlement data. Users are responsible for lawful access to source data and compliance with platform terms.

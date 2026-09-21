---
name: sellersprite-bi-market-research
description: 使用卖家精灵（SellerSprite）从种子关键词与核心竞品 ASIN 扩展关键词和相似产品，按标题、Listing 属性、类目与人工规则筛选目标 ASIN，再结合标准/详细导出制作可追溯、父 ASIN 去重、年度/YTD/同比、类目/属性、品牌销售额竞争和排名动量的 Amazon 交互式 HTML BI。适用于“关键词+竞品找相似品”“筛选目标 ASIN”“Listing 属性筛选”“卖家精灵品类 BI”“父体去重”“品牌竞争”等请求；不适用于 Listing 文案、个人购物推荐、无市场研究范围的简单图表，或把关键词结果直接当完整类目 TAM。
---

# SellerSprite 品类 BI 市场研究

## Purpose And Scope

将 SellerSprite 的标准导出、详细导出和用户提供的参考 BI，转换为可复核的数据层与单文件交互式 HTML 看板。SellerSprite 数据是第三方估算，不是 Amazon 结算数据；所有结论必须能追溯到输入文件、范围清单、公式和缺失说明。

固定区分三个市场层：

1. `Category Baseline`：经过验证的品类大盘，用于说明总体容量。
2. `Core Direct Market`：解决同一任务、适配范围和产品结构相近的直接竞争父体。
3. `Adjacent/Substitute Market`：低价通用件、结构不同的替代品、附件、替换件或关键词误匹配。

车型项目还必须固定车型、代际、年份、站点和适配边界。项目级可疑品牌、排除项和例外规则只写入该项目的 scope manifest，不得硬编码为所有品类的通用规则。

## Use Cases

### Use Case 1: 新建品类 BI

- Trigger: “用卖家精灵做一个汽车配件品类 BI 看板。”
- Inputs: 品类/车型边界、站点、标准导出、详细导出、数据截止日。
- Steps: 冻结范围，父体去重，计算年度/同比/品牌销售额竞争，生成交互式 HTML。
- Result: 可直接打开的单文件 HTML、标准化 JSON/CSV、范围与数据质量说明。

### Use Case 2: 校准已有 BI

- Trigger: “把我导出的 BI 跟 SellerSprite 数据核对，并补齐缺少维度。”
- Inputs: 现有 BI、SellerSprite 导出、已知排除项与统计口径。
- Steps: 对比 ASIN 范围、父子体口径、时间覆盖、销售额方法和类目维度，输出差异并重建看板。
- Result: 保留旧版本的新 HTML、差异清单、修正后的数据层和校准记录。

### Use Case 3: 增加独立排名动量

- Trigger: “在车型 BI 里增加全局产品排名变化，但不要混入商业机会评分。”
- Inputs: 至少连续 6 个完整月的父体月销售额，默认前 3 个月对比后 3 个月。
- Steps: 仅纳入六个月均有观测值的父体，建立固定全局分母，计算前后窗口排名和名次变化。
- Result: 独立排名页、完整可分页明细、50/100/250/全部行选项；筛选不重算全局排名。

### Use Case 4: 从关键词和核心竞品建立 ASIN 范围

- Trigger: “我给你一个关键词和竞品 ASIN，找相似产品、收集关键词、按 Listing 属性筛掉无关产品，再做 BI。”
- Inputs: 站点、种子关键词、核心竞品 ASIN、产品任务边界、SellerSprite 关键词/竞品导出、项目筛选规则。
- Steps: 聚类关键词，合并高频 ASIN 与竞品候选，抽取标题/Listing 属性，分为核心/相邻/排除/复核，确认目标父子 ASIN 后再导出和规范化。
- Result: `keyword_evidence.csv`、候选/父体 scope manifest、目标 ASIN 清单、分层规范化数据与单文件 BI。
- Worked method: 当任务形态接近“AI 录音设备 + 转录/总结”时，阅读 [references/worked-example-ai-voice-recorder.md](references/worked-example-ai-voice-recorder.md)，复用其发现、证据、四层筛选、详细覆盖闸门与 BI 方法，但不得把案例中的品牌、关键词或排除词当作其他品类的全局规则。

## Implementation Basis And Dependencies

本 skill 可行的基础是 SellerSprite 关键词挖掘和竞品标准导出支持候选发现，详细导出包含按月销量、销售额和历史价格，标准导出补充父子 ASIN、品牌、图片、标题、Listing 属性、链接、评分、评论、上架时间和类目。发现与规范化脚本使用 Python 与 `openpyxl`，看板使用内联 CSS/JavaScript/SVG 或 Canvas，在 `file://` 下运行。

| Dependency | Requirement / Provider | Purpose | Availability Check And Missing Behavior |
| --- | --- | --- | --- |
| SellerSprite 授权账号 | 新鲜采集时条件必需；用户提供 | 登录和导出 | 登录前确认账号获得授权；占用时只轮换用户明确提供的其他账号。无账号时仅处理现有导出，不保存凭证。 |
| SellerSprite 标准导出 | 元数据分析时条件必需；用户或在线导出 | 品牌、图片、链接、父子体与当前快照 | 用 `openpyxl` 验证可打开、非空且含有效 ASIN；缺失时标记品牌/图片/当前元数据不完整。 |
| SellerSprite 关键词挖掘导出 | 从关键词/竞品发现时条件必需；用户或在线导出 | 关键词聚类、需求/竞争证据与高频 ASIN | 校验关键词、时期和指标列；缺失时可从 ASIN/竞品开始，但不得声称完成关键词覆盖。 |
| SellerSprite 详细导出 | 多年度 BI 必需；用户或在线导出 | 月销量、月销售额、历史价格 | 验证 `YYYY-MM` 列和目标工作表；只有 30 天快照时降级，不虚构年度趋势。 |
| Python 3 + `openpyxl` | 规范化必需；宿主环境 | 运行规范化与测试脚本 | 运行版本/导入检查；缺失时停止自动规范化并报告安装依赖。 |
| 浏览器或 Playwright | 在线采集时条件必需；宿主环境 | 隔离登录、查询、导出和验证 | 检查可用浏览器能力；不可用时请求现有导出，不操作用户已有标签页。 |
| 参考 BI/XLSX/HTML | 可选；用户提供 | 口径、维度与结果校准 | 验证文件/链接可读；缺失时跳过参考差异分析，不影响基础规范化。 |
| Amazon 图片/商品链接 | 可选增强；标准导出或 Amazon | 父 ASIN 识别和钻取 | 检查 URL 和图片回退；加载失败时保留 ASIN、标题与链接文本。 |
| Feishu MCP | 仅飞书交付时条件必需；宿主配置 | 写入 Bitable/Sheets/Docs/Drive | 先检查 MCP 对应 OpenAPI；能力缺失时停止飞书写入并请求明确方向，不自行打开网页。 |
| 网络与站点权限 | 在线采集时条件必需；用户/环境 | 访问 SellerSprite 和 Amazon | 通过只读访问或登录结果确认；阻断时保留已有证据并报告具体停止点。 |

不得安装 Power BI。静态交付默认是一个可直接打开的自包含 `.html`，不启动 localhost；只有用户明确要求或功能确实依赖 HTTP/服务端时才使用服务器。

## Inputs

| Input | Purpose / Requirement | Type, Source, Example | Validation, Default, Missing Behavior | Sensitivity / Authorization |
| --- | --- | --- | --- | --- |
| `scope_manifest` | 冻结统计边界；必需 | JSON/CSV/Markdown，用户/研究过程；如 `Amazon US / L3 / target vehicle generation and years` | 必含品类、车型/代际、国家、L2/L3/叶子、包含/排除、查询链接、截止日；缺失时先建立，边界不明则停止容量判断。 | 低敏；排除品牌仅限当前项目。 |
| `seed_keyword` | 启动关键词扩展；发现型任务必需 | 字符串，用户；如 `ai voice recorder` | 校验站点语言与产品任务；过宽时用核心竞品和长尾聚类收窄，不把它直接定义为类目。 | 无。 |
| `seed_asins` | 锚定核心产品与相似品；发现型任务至少 1 个 | ASIN 列表/URL，用户；如 `B0FYQ4Y2ZZ` | 校验 10 位 ASIN、站点和 Listing 是否对应目标任务；不可访问时保留用户声明并降低证据等级。 | 无。 |
| `keyword_export` | 关键词聚类与高频 ASIN；发现型任务条件必需 | SellerSprite Keyword Mining XLSX | 校验非空、关键词、搜索量和高频 ASIN 列；缺失时标记关键词层不完整。 | 可能反映内部选品方向。 |
| `discovery_rules` | 让相关性筛选可复核；发现型任务必需 | JSON；类目、核心/相邻/排除词、品牌、ASIN 覆盖规则 | 规则只适用于当前项目；必须复核高销售额排除项和 `review`，不得把品牌规则全局化。 | 低敏；可能含内部策略。 |
| `standard.xlsx` | 补足元数据；条件必需 | SellerSprite `Export`，用户或在线导出 | 校验非空、可打开、含有效 ASIN；缺失时输出可用月度数据，但品牌、图片和当前快照不完整。 | 可能含内部研究范围；不得包含凭证。 |
| `detail.xlsx` | 构建多年度事实表；多年度 BI 必需 | SellerSprite `Export details`，用户或在线导出 | 至少有 `YYYY-MM` 列；无文件则降级快照，无销售额页则相关指标为 `N/A`。 | 同上。 |
| `as_of` | 确定完成月；必需 | `YYYY-MM-DD`；如 `2026-09-21` | 默认执行日；无效日期停止；最后完成月为所在月前一个月。 | 无。 |
| `marketplace` | 隔离站点统计；必需 | 字符串；如 `Amazon US` | 必须明确；US/CA/MX 不自动合并，未采集市场显示 `N/A`。 | 无。 |
| `category_and_fitment_map` | 支持类目/车型筛选；车型或多类目项目条件必需 | CSV/JSON，用户/Listing；含 L2/L3/叶子、车型、代际、年份 | 校验枚举和未知值；缺失时保留 `Unknown`，车型边界不明则停止车型结论。 | 无。 |
| `type_map` | 稳定产品结构分类；推荐 | CSV/JSON，父/子 ASIN 到类型 | 冲突需人工规则；缺失映射保留 `Unknown`，不按价格猜测。 | 无。 |
| `reference_bi` | 校准维度和口径；可选 | XLSX/HTML/链接，用户提供 | 校验可读并只作为来源证据；缺失时跳过差异分析。 | 可能含内部业务数据。 |
| `keyword_evidence` | 解释需求与流量；Basic BI 推荐 | SellerSprite 页面/导出；搜索量、购买率、PPC 等 | 校验时期和关键词；缺失时标记关键词层空缺，不替代 ASIN 销量。 | 无。 |
| `rank_window_months` | 定义前后排名窗口；可选 | 正整数；默认 `3` | 至少 1；需要连续 `2 x window` 完成月，不足则排名为 `N/A`。 | 无。 |

运行时用户名、密码、Cookie、Token、浏览器存储和本地用户配置路径不得进入 skill、命令历史、导出包、截图、日志或 HTML。

## Outputs

| Output | Meaning / Format | Destination | Acceptance Criteria / Failure Behavior |
| --- | --- | --- | --- |
| `dashboard_data.json` | 看板统一数据对象 | 规范化输出目录 | 包含元数据、父体月度、市场月度、年度、同周期、竞争、排名动量和质量信息；所有视图从同一对象计算。 |
| `keyword_evidence.csv` | 聚类后的关键词需求/竞争证据 | 发现输出目录 | 含 cluster、相关性、搜索量、增长、购买率、商品数、PPC 和高频 ASIN；不将购买量当销量。 |
| `candidate_manifest.csv` | 子 ASIN 发现与筛选审计 | 同上 | 每行含父体、决策、得分、原因、详细导出覆盖、标题/类目/Listing 属性；排除项仍保留。 |
| `parent_scope_manifest.csv` | 父 ASIN 去重后的候选范围 | 同上 | 同父体合并，保留子 ASIN 数量、代表商品与市场层；用于 BI 边界复核。 |
| `target_child_asins.txt` | 可提交详细导出的目标子 ASIN | 同上 | 默认仅含 `core_direct` 且有详细导出覆盖的 ASIN；缺覆盖时单独列为待补采。 |
| `parent_monthly.csv` | 父 ASIN + 月份的销量、销售额、模拟 GMV | 同上 | 同父体子体不相加；真实 0 保留；缺失留空。 |
| `market_monthly.csv` | 月度市场汇总及同比 | 同上 | 与父体月度求和一致，销售额和模拟 GMV 分列。 |
| `parent_current.csv` | 最新完整月父体竞争明细 | 同上 | 含图片/链接元数据、销量、SellerSprite 销售额及份额。 |
| `rank_momentum.csv` | 固定全局分母的前后窗口排名 | 同上 | 缺任一所需月份的父体被排除；正值代表排名改善；标注不是 Amazon BSR。 |
| `conflicts.csv` | 子体历史冲突审计 | 同上 | 按 `units` 与 `seller_sprite_sales_amount` 分开记录选值和原始子体值。 |
| `dashboard.html` | 单文件交互式品类 BI | 用户指定目录或项目输出目录 | `file://` 可打开，无外部 CDN/本地接口依赖，筛选联动、钻取、图片回退、分页和移动端可用。 |
| `scope-and-quality` | 范围、来源、公式、不确定性与差异说明 | HTML 底部和证据包 | 文字说明下沉；关键警告用标注或悬浮提示，不挤占数据主界面。 |

失败或部分完成时必须输出已有的规范化结果与明确缺口，不得将缺失值写成 0、用评论数/BSR/关键词购买量补历史，或把小样本宣称为完整品类容量。

默认副作用仅限在用户指定或项目输出目录写入新文件；不会删除旧看板、修改 SellerSprite/Amazon 数据或发送通知。只有用户明确要求飞书交付时才通过 Feishu MCP 写入外部系统，并报告所创建或替换的对象。

## Workflow

1. 若输入是种子关键词 + 核心竞品，先阅读 [references/discovery-and-relevance-workflow.md](references/discovery-and-relevance-workflow.md)：定义产品任务，导出关键词和竞品标准表，聚类关键词，抽取 Listing 属性，并生成核心/相邻/排除/复核 manifest。AI 录音设备类任务同时阅读 [references/worked-example-ai-voice-recorder.md](references/worked-example-ai-voice-recorder.md)，将案例方法转写为本项目 scope manifest；已有明确 ASIN 范围时可跳到第 3 步。
2. 运行 `scripts/discover_sellersprite_market.py`；人工复核所有 `review` 与高销售额排除项。关键词/搜索结果只用于发现与需求证据，不视为类目 TAM。
3. 阅读 [references/collection-workflow.md](references/collection-workflow.md)，冻结站点、国家、类目、产品任务、属性、车型/适配、时间和排除边界。修订现有看板时保留旧的用户版本。
4. 若需要在线采集，用隔离浏览器会话登录授权 SellerSprite 账号，对每个市场层同时导出标准文件与详细文件；记录提交 ASIN、返回 ASIN、批次和缺失项。
5. 阅读 [references/data-contract.md](references/data-contract.md)，分别对 `category_baseline`、`core_direct` 和必要的 `adjacent_substitute` 运行：

```powershell
python scripts/normalize_sellersprite_exports.py `
  --standard "path/to/standard.xlsx" `
  --detail "path/to/detail.xlsx" `
  --scope-manifest "path/to/candidate_manifest.csv" `
  --include-decisions "core_direct" `
  --output-dir "path/to/normalized" `
  --as-of 2026-09-21 `
  --market-name "Category or vehicle name" `
  --marketplace "Amazon US" `
  --rank-window-months 3
```

6. 以父 ASIN 为销售统计粒度；共享子体按父体 + 月份取可见最大值并留冲突记录。标准表元数据只能进入详细表覆盖的父/子 ASIN，防止未选候选膨胀父体数。销量、SellerSprite 销售额、价格和模拟 GMV 不得混为同一个指标。
7. 年度数据按年拆分；完整年、部分年、YTD、同周期同比使用准确月集。为包含 12 月的全年报告补采 12 月，和旧导出按 ASIN/父体/月去重核对。
8. 品牌竞争默认按父体去重后的 SellerSprite 销售额；无销售额页时显示 `N/A`，不自动退回销量或模拟 GMV。
9. 商业机会页使用关键词需求、增长、竞争、价格/利润、产品属性、产品结构和证据质量。排名动量是单独页面/维度，不得静默混入机会评分。
10. 阅读 [references/dashboard-standard.md](references/dashboard-standard.md)，生成一个直接打开的自包含 HTML，使用图表优先、文本下沉的纯数据界面，并提供市场层、关键词簇和项目属性筛选。
11. 对照参考 BI 核对总量、范围、父子体、年度、L3、品牌销售额、属性、车型和国家覆盖。将无法解释的异常品牌放入项目级复核/排除清单，不作全局规则。
12. 在桌面和移动端检查图表非空、筛选联动、钻取、图片、分页、控制台、编码、溢出和凭证泄漏；再执行发现/规范化脚本测试、触发/非触发检查与 skill 验证。

## Non-Negotiable Data Rules

- 父 ASIN 是销量和销售额统计粒度；兄弟子体永不相加。
- 关键词和竞品搜索结果是发现样本，不是完整品类 TAM；容量结论需要单独验证的 baseline。
- 每个候选保留 `core_direct`、`adjacent_substitute`、`excluded_noise` 或 `review` 及其原因；排除项不得静默删除。
- 标题和 Listing 属性可用于筛选，但缺失属性保留 `Unknown`，不得按价格或品牌臆测。
- 标准导出比详细导出更宽时，未出现在详细覆盖范围的产品不得进入销售父体数和份额分母。
- 完整年、部分年、YTD 和同周期同比必须分开，月集不一致时不计算同比。
- 品牌竞争的默认口径是父体去重后的 SellerSprite 销售额。
- 保留 L2、L3 和叶子类目，L3 必须可筛选和对比。
- 商品明细必须显示父 ASIN、代表图片、品牌、标题、链接、父子关系和主要指标。
- US/CA/MX 分开采集和显示；未覆盖市场是 `N/A`，不是 0。
- 全局排名动量仅使用完整父体样本：`rank_change = prior_global_rank - recent_global_rank`，正值代表改善。
- 看板筛选只限制显示候选，不重算全局排名分母；排名页必须支持 50/100/250/全部和完整分页。
- 排名动量标注为“样本销售额计算排名，不是 Amazon BSR”。
- 观察值 0 是有效数据；空白/未返回是缺失，两者不可互换。
- 所有指标标注为 `Observed`、`Calculated`、`Modeled`、`Inference` 或 `N/A`。

## Error And Stop Conditions

- 只有标准导出、没有详细导出：降级为当前快照，停止年度/同比结论。
- 详细导出没有销售额页：销量与模拟 GMV可以继续，品牌销售额竞争和排名动量为 `N/A`。
- 品类/车型边界无法确定：停止容量和机会结论，先输出待确认范围。
- `review` 候选或高销售额排除项未复核：停止发布核心市场总量，先输出候选 manifest 和待确认清单。
- 关键词导出缺失：可继续已知 ASIN 的竞品 BI，但必须标记关键词覆盖未完成。
- 参考 BI 与导出差异无法由时间、范围或粒度解释：标记异常，不强行调平。
- 国家站点未采集：显示 `N/A`，不跨站点外推。
- 依赖、权限、网络或授权缺失：报告具体失败步骤和可用的部分产物，不绕过权限。

## Functional Validation Scenarios

- Given: 有效标准导出、含销量/销售额/价格的详细导出和明确范围；When: 运行规范化与 HTML 构建；Then: 六类规范化文件和单文件看板存在，父体月度汇总、年度、竞争与排名均通过对账。
- Given: 标准导出缺失但详细导出有效；When: 规范化；Then: 保留月度销量/销售额，品牌、图片和当前元数据标为不完整，不伪造字段。
- Given: 详细导出缺少销售额页；When: 构建 BI；Then: 销量和模拟 GMV 可继续，品牌销售额竞争与排名动量明确为 `N/A`。
- Given: 车型/品类边界未定义；When: 请求市场容量或机会结论；Then: 停止该结论，先产出待确认范围，不把关键词结果当品类大盘。
- Given: 一个种子关键词、核心竞品和 SellerSprite 关键词/竞品导出；When: 运行发现脚本；Then: 输出关键词聚类、四层候选 manifest、Listing 属性和有详细覆盖的目标 ASIN 清单。
- Given: `ai voice recorder`、`B0FYQ4Y2ZZ` 和对应 SellerSprite 导出；When: 按 worked example 建立范围；Then: 将“录音 + 转录/总结等 AI 信息结果”与“仅 AI 降噪的传统录音笔”、附件及无关捆绑分层，只有详细导出覆盖的已接受 ASIN 进入 BI 销售分母，并明确该查询样本不是品类 TAM。
- Given: 与录音设备无关的新产品品类；When: 复用 worked example；Then: 只复用流程、证据结构和覆盖闸门，重新定义产品任务、属性、关键词与排除规则，不继承 Plaud、录音笔或订阅相关的项目规则。
- Given: 标准导出包含 900 个候选但详细导出只含 60 个；When: 规范化；Then: 只有详细表覆盖且被 scope manifest 接受的父/子 ASIN 进入销量、销售额、父体数和份额分母。
- Given: SellerSprite 登录、网络或导出失败；When: 在线采集；Then: 记录失败步骤，保留已有导出和旧看板，关闭代理创建的临时页面，不绕过访问控制。

## Definition Of Done

- 输入文件、范围清单、时间覆盖、站点和来源均可追溯。
- 种子关键词/ASIN、关键词簇、候选来源、相关性决策、原因、属性与目标 ASIN 均可追溯。
- 父体去重、冲突、缺失和真实 0 已通过审计。
- 年度、YTD、同周期同比、销售额、模拟 GMV和 ASP 名称准确且互不混淆。
- 品牌竞争按销售额，L3/车型/国家边界明确，父 ASIN 图片与钻取可用。
- 商业机会与排名动量分离，排名分母固定并可浏览全部记录。
- HTML 单文件可直接打开，不依赖 localhost、外部 CDN 或本地接口；旧版本未删除。
- 桌面/移动 QA、脚本测试、触发/非触发检查和 `quick_validate.py` 全部通过。

## References

- [SellerSprite Collection Workflow](references/collection-workflow.md)
- [Keyword Discovery And Relevance Workflow](references/discovery-and-relevance-workflow.md)
- [Worked Example: AI Voice Recorder Market Discovery To BI](references/worked-example-ai-voice-recorder.md)
- [SellerSprite Data Contract](references/data-contract.md)
- [BI Dashboard Standard](references/dashboard-standard.md)

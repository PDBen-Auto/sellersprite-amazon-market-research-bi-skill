# 卖家精灵市场研究与BI

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

按用户明确指定的语言输出，否则跟随请求语言。保留命令、技能 ID、JSON 键、枚举值、单位和来源原文；翻译与原文分开，不通过语言推定国家、币种或司法辖区。先读取完整规范中与任务相关的详细引用，执行原有校验和授权要求。

## 安装与使用

下载或克隆仓库，将下列技能目录连同其 references、scripts、assets 等现有依赖一起放入宿主的技能目录。保留目录名和 SKILL.md；仅更换说明语言无需重复安装。安装命令供用户自行选择，不表示已安装或启用。

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## 卖家精灵市场研究与BI

`sellersprite-bi-market-research`

由种子意图扩展相关ASIN，分市场层并按父体去重，制作可审计导出BI。

技能目录: `.`

**实现依据与依赖**

明确市场/产品任务、标准/详细XLSX及按需关键词表；脚本需Python3与openpyxl；在线需获准SellerSprite账号/浏览器；估算不是Amazon结算。

**输入**

范围/日期/站点/纳排规则；发现需seed_keyword/seed_asins；按需关键词、标准和详细导出；可选相关性规则、属性和输出位置；禁止凭证。

**输出**

有原因和详细覆盖的候选manifest；父体/月度/年度/YTD/同期/品牌销售额/排名动量数据；自包含dashboard.html、审计和缺失记录。

[执行流程 · 边界与停止条件 · 示例请求](references/i18n/zh-CN.md)

> 请使用 `$sellersprite-bi-market-research` — 从关键词和竞品导出制作核心市场看板，不把未有详细覆盖的候选计入销售分母；用简体中文输出，保留证据、未知项与操作边界。

## 语言覆盖与验证

这是本技能的本地化操作指南，覆盖用途、依赖、输入输出、步骤、示例及边界，不是全部引用文档的逐句翻译。详细技术引用、历史案例、脚本错误、示例网页及图片保留原文；助手可按请求解释它们。本次文档经过结构、链接和关键约束核对，尚无逐语种母语人工审校。

交付前逐项核对输入、证据、缺失值、输出文件和原有完成标准；未执行的步骤标为未验证，不把脚本退出成功当业务成功。

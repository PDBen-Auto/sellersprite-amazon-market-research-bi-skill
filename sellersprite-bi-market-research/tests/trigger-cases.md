# Trigger Cases

## Should Trigger

- “我给你一个关键词和核心竞品 ASIN，先找相关产品和关键词，筛掉不相关 Listing，再做 SellerSprite BI。”
- “Use this competitor ASIN to discover similar products, cluster keywords, filter by title attributes, and build a parent-deduplicated market dashboard.”
- “根据卖家精灵标准/详细导出，把 AI note taker 与只做降噪的传统录音笔分层，做品牌销售额和年度趋势看板。”
- “以 ai voice recorder 和 B0FYQ4Y2ZZ 为种子，扩关键词、找相似品，按转录/总结、订阅和形态筛选后做 BI。”
- “做一个 SellerSprite category BI，支持三级类目、产品属性、车型/适配、父 ASIN 和市场层筛选。”

## Should Not Trigger

- “帮我重写这个 Amazon Listing 的五点描述。”
- “用这 5 个数字画一个简单柱状图，不需要市场研究或 SellerSprite 数据。”
- “推荐几款会议录音笔给我个人购买。”
- “把 Plaud 的品牌和排除词硬编码成所有 Amazon 品类的通用筛选规则。”

## Boundary Notes

The skill should activate for SellerSprite/Amazon category intelligence that needs keyword/ASIN discovery, relevance filtering, parent-level normalization, or an auditable BI. Pure copywriting, consumer shopping advice, and generic charting should route elsewhere.

The AI Voice Recorder worked example is an illustrative execution pattern. It must not cause recorder-specific keywords, brands, subscription attributes, or exclusions to be inherited by unrelated categories.

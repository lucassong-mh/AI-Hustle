# [AI又卷了] OpenAI内部备忘录曝光：Anthropic 300亿收入有80亿是假的

![封面](https://platform.theverge.com/wp-content/uploads/sites/2/2025/04/STK_414_AI_CHATBOT_R2_CVirginia_B.jpg?quality=90&strip=all&crop=0%2C0%2C100%2C100&w=1200)

4月13日，OpenAI首席营收官Denise Dressler发了一封四页内部备忘录，标题是"The System That Will Win Enterprise AI"。备忘录本来是给自家员工打气的，但里面关于Anthropic的那段话，瞬间引爆了整个科技圈。

## 核心指控：80亿美元的水分

备忘录中最具杀伤力的段落是这样的：

> "他们的stated run rate是虚高的。他们使用的会计处理方式让收入看起来比实际更大，包括把与Amazon和Google的分成收入gross up。我们的分析显示，这把他们的run rate虚报了大约80亿美元（在他们声称的300亿美元基础上）。"

翻译成人话：Anthropic说自己的年化收入是300亿美元，但OpenAI认为其中80亿是虚高的——如果按照更保守的会计标准，Anthropic的真实收入大概在220亿美元左右，并不比OpenAI的240亿高出多少。

## 这80亿是怎么来的？

关键在于一种叫做"gross vs net"的会计分歧。

Anthropic通过AWS Bedrock、Google Cloud Vertex AI和Microsoft Azure三个云平台分发Claude。当用户通过这些平台付费使用Claude时，Anthropic把**全部金额**（包括云平台的分成部分）先记为收入，再把云平台的那部分列为销售和营销费用。这叫gross reporting——Anthropic是交易的主体，云平台只是渠道。

OpenAI的做法不同。它把Microsoft Azure的分成部分先扣掉，只把净额列为收入。这叫net reporting——Microsoft是交易的主体，OpenAI是供应商。

两种做法在美国GAAP下都合规。关键在于你在每笔交易中是"principal"还是"agent"。Anthropic认为自己是principal，OpenAI认为自己在Azure上是agent。但两种方式算出来的结果，差了整整80亿。

## 备忘录还说了什么？

 Dressler的备忘录不止是抨击Anthropic。它更像是OpenAI的企业版作战地图：

1. **模型层赢企业**——新模型代号"Spud"被描述为"我们最聪明的模型"，要强化推理和执行能力
2. **Agent平台层**——内部代号"Frontier"，要成为企业Agent的默认平台
3. **Amazon渠道**——备忘录称与Amazon的合作上线后需求"惊人"，Amazon还投了500亿美元
4. **全栈销售**——ChatGPT for Work、Codex、API、Frontier、Amazon运行时，整套卖
5. **部署为王**——内部代号"DeployCo"，帮企业把模型真正用起来

关于Anthropic，备忘录还提到：
- Anthropic"没买到足够的compute"是战略失误，导致限流和可用性下降
- "他们的coding focus给了他们一个早期切口，但你不应该在一个平台战争中做单产品公司"
- "他们的叙事建立在恐惧、限制和精英控制AI的理念上"

## 另一面：预测市场更看好Anthropic

Dressler的备忘录写得气势汹汹，但市场数据讲了一个不同的故事：

- Kalshi和Polymarket预测市场给Anthropic **59%的概率**在6月前拥有排名第一的AI模型，OpenAI只有6%
- Polymarket给Anthropic **66%的概率**比OpenAI先上市
- Anthropic在二次市场的股票需求"接近疯狂"，OpenAI的股票却在折价交易
- 有同时投资两家的VC告诉FT，OpenAI的8520亿美元估值需要假设IPO价格超过1.2万亿美元，而Anthropic的3800亿估值反而像是"捡了便宜"

## 还有一层微妙的

OpenAI自己的营收计算也不是完全没有争议。微软和OpenAI的关系越来越微妙——备忘录里说微软合作"基础但限制了我们的触达"，而微软在2024年中期就把OpenAI列入了竞争对手名单。OpenAI正在转向Amazon、CoreWeave、Google、Oracle寻求更多算力。

与此同时，Anthropic签下了与Google和Broadcom的长期协议，锁定3.5吉瓦TPU算力，2027年开始交付。Anthropic还是唯一一个同时入驻三家主流云平台的frontier模型。HumanX大会上，Glean CEO用"Claude狂热"和"一种宗教"来形容市场对Claude的需求。

两家公司都计划今年上市。不管谁先提交S-1文件，收入计算方式的差异都会被监管机构放大检视。Dressler的备忘录与其说是攻击Anthropic，不如说是在IPO前给投资者讲一个"我们才是正经人"的故事。

---

*参考资料：The Verge《Read OpenAI's latest internal memo about beating the competition》(2026.4.13) | CNBC《OpenAI touts Amazon alliance in memo》(2026.4.13) | TechCrunch《Anthropic's rise is giving some OpenAI investors second thoughts》(2026.4.14) | Forbes《OpenAI And Anthropic Count Revenue Differently》(2026.3.25)*

---

两家AI公司抢着说自己赚得多，这本身就是2026年最荒诞的叙事之一。一年前它们还都在烧钱，现在就开始争谁的账面收入更实——这说明资本市场对AI的定价已经从"讲技术故事"进入"讲财务故事"的阶段了。

但那80亿美元的分歧点才是真正有意思的地方。gross和net在GAAP下都合规，这意味着监管部门也不会给你一个黑白分明的答案。真正的裁判是IPO时的二级市场——到时候如果Anthropic的定价不能支撑300亿年化收入的乘数，那80亿的虚高就会变成实实在在的估值折损。反过来，如果市场对Claude的认知需求足够旺盛，谁在乎你怎么记账？

Dressler的备忘录与其说是揭穿Anthropic，不如说是OpenAI在对自己的投资者说："别被他们的数字吓到，我们才是更老实的那一个。"在两家都准备上市的当下，这番话的目标听众不是员工，是华尔街。
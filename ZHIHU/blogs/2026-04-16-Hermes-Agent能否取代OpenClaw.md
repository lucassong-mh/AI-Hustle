# [开源万岁] 6周涨到8万star，Hermes会杀死OpenClaw吗？

![封面](https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200&q=80)

2月25日，一个叫Hermes Agent的项目在GitHub上静悄悄地上线，配了一条简单的推文："Meet Hermes Agent, the open source agent that grows with you."

六周后，它有了8万颗星。

## 什么是Hermes Agent？

Hermes Agent是Nous Research开发的开放式AI Agent框架。Nous Research是个大约20人的研究实验室，由Teknium领衔——这个名字在开源AI圈里不陌生，他们之前做的Hermes系列fine-tuned模型在Hugging Face上就有大量拥趸。

项目用Python写成，核心只有约9200行代码，MIT协议，完全开源。

听起来没什么特别的对吧？别急。

## 它凭什么6周8万星？

Hermes的核心卖点只有一个词：**自学习**。

你让它完成一个任务，它做完之后会自动生成一份skill document——记录自己是怎么做的，下次遇到类似任务直接调用，速度提升约40%。这不是简单的prompt缓存，而是一个持续自我改进的循环：做完→记录→下次更快→记录优化→再快。

这个"自学习循环"是OpenClaw完全没有的东西。

然后是时机。4月3日，Anthropic封锁了OpenClaw访问Claude的订阅权限，这条新闻冲上Hacker News头条。Nous Research立刻发了一条推：

> "If you're having trouble with your lobster-themed agent since the recent update, try downloading Hermes Agent, then running hermes claw migrate. We've been told this helps a lot."

这条推拿到了813个赞。一夜之间，大量OpenClaw用户跑来试Hermes。

## 6周迭代8个版本

| 版本 | 时间 | 关键变化 |
|------|------|---------|
| v0.1 | 2月25日 | 初始发布 |
| v0.5 | 3月中 | 三层记忆架构上线 |
| v0.8 | 4月8日 | 模型实时切换、MCP OAuth 2.1、209个PR |
| v0.9 | 4月13日 | 487次commit、269个PR、63,281行新增 |

这速度对比一下：OpenClaw的社区版从发布到万星用了几个月，Hermes用了一周。

## 三层记忆 vs 一个MEMORY.md

这是技术上最关键的差异。

OpenClaw的记忆方式是一个扁平的MEMORY.md文件——什么都往里塞，越用越大，没有边界，没有索引，慢慢就变成了一个无人维护的垃圾场。

Hermes的设计完全不同：

- **Session Memory**——当前会话上下文，关闭即清
- **Persistent Memory**——严格受限，MEMORY.md限2200字符，USER.md限1375字符。逼Agent做减法而非加法
- **Skill Memory**——自动生成的技能文档，存入SQLite全文检索

还有8个可插拔的外部记忆后端：Honcho、Mem0、Hindsight、Supermemory等，随你选。

## 安全：0 vs 9

3月份，OpenClaw在4天内被曝出9个安全漏洞，最高评分CVSS 9.9/10。全球有13.5万个暴露实例，ClawHub上800多个恶意技能。这对企业用户来说是噩梦级的数据。

Hermes至今0个Agent相关CVE。

这个对比过于戏剧化，但它确实成了很多用户迁移的决定性因素。

## 成本：月付10美元 vs 月付30美元

Hermes可以跑在一台5美元/月的VPS上。加上市面上的serverless后端（Modal、Daytona），典型月成本10-25美元。OpenClaw的典型月成本在20-32美元之间。

而且Hermes默认支持多个模型后端——你可以中途切换模型，不再被锁死在Claude上。

## 但先别急下结论

Hermes目前的短板也很明显：

- **平台覆盖只有6-14个**，OpenClaw是50+个——企业要的是全平台接入，这点Hermes还差得远
- **没有企业级支持**，没有NVIDIA NemoClaw，也没有OpenAI这样的重量级盟友
- **Token开销比OpenClaw高15-25%**——自学习循环每次都要反思和记录，这不是免费的
- **OpenClaw有4万多个社区技能**，Hermes的生态才刚起步

更诚实的说法是：它们目前服务于不同的场景。Claude Code在IDE里写代码，OpenClaw在团队协作里做运维自动化，Hermes在学习型个人Agent这个细分里长得最快。

## 它会杀死OpenClaw吗？

不会。但会让OpenClaw很难受。

Hermes的周新增星数约9500，OpenClaw约3000。如果这个速率差持续，今年夏天两者就会在star数上持平。这会改变开发者社区的叙事——"Hermes是未来"会成为一种自我实现的预言。

更关键的是，Hermes证明了一件事：开源AI Agent的核心竞争力不应该是"接多少平台"，而应该是"能不能越来越聪明"。自学习循环是Agent从工具变成伙伴的分界线。OpenClaw接了50个平台，但它永远不会比昨天更聪明。Hermes会。

---

*参考资料：NousResearch/hermes-agent (GitHub) | Hermes Atlas《State of Hermes Report》(2026.4.11) | The Verge《Anthropic temporarily banned OpenClaw's creator》(2026.4.3) | DeployAgents comparison | 多篇中英文深度评测*

---

OpenClaw接了50个平台，但它永远不会比昨天更聪明。Hermes接了6个，但它每天都在变快。

这不是一个"谁杀谁"的故事。这是一个"Agent是从工具进化还是从平台堆砌"的路线之争。OpenClaw的选择是广度——我能连到一切。Hermes的选择是深度——我能记住你，能学会，能自我改进。

6周8万star说明了市场正在投票。但真正的考验不是GitHub上的星星数，而是哪个框架能让Agent在用了一百次之后，真的变成一个你离不开的东西。在那之前，所有star都只是围观。
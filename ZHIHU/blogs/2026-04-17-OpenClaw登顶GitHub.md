# [越封越火] 60天超越Linux和React十年+的star，OpenClaw凭什么？

![封面](https://openclaw.ai/og-image.png)

3月3日，OpenClaw以约25万颗GitHub星超越React，成为GitHub史上star最多的软件项目。

React攒这些星花了11年。OpenClaw用了60天。

这个数字本身就值得停下来想一想。

## OpenClaw是什么

一个MIT协议的开源个人AI助手框架，用TypeScript写的monorepo。你可以连WhatsApp、Telegram、Slack、Discord、微信、QQ等25+个平台，让一个AI Agent帮你处理消息、跑任务、写代码、管日程。

它最初叫Clawdbot，2025年11月由奥地利开发者Peter Steinberger（@steipete）发布。后来改名Moltbot，再改名OpenClaw。龙虾吉祥物"Lobster"是它的标志性梗——所以叫OpenClaw。

现在由OpenClaw基金会管理，赞助商包括OpenAI、GitHub、NVIDIA、Vercel。

## 60天25万星是怎么做到的

看几个关键节点：

- **2025年11月**：以Clawdbot之名上线
- **2026年1月**：更名OpenClaw，病毒式增长开始
- **2月15日**：创始人Steinberger加入OpenAI（这是后话）
- **2月19日**：Anthropic封锁所有第三方工具的Claude Pro/Max OAuth访问——OpenClaw首当其冲
- **2月24日**：超越Linux内核，224K vs 218K星
- **3月3日**：超越React，~250K星
- **4月4日**：Anthropic宣布Claude订阅不允许覆盖OpenClaw使用，用户面临50倍价格飙升——即"claw tax"
- **4月10日**：Anthropic暂时封禁Steinberger个人Claude账号，几小时后恢复
- **4月17日**：359K星，73K fork，还在涨

增长曲线几乎完美对应每次Anthropic的"打击"——2月封锁OAuth，星数暴涨；4月收claw tax，星数又暴涨。Anthropic每推一把，就有更多用户涌入OpenClaw。

Steinberger在拒绝加入Anthropic时说了一句："一边欢迎我，一边发律师函。"

## 争议：安全、成本、和"到底归谁管"

OpenClaw现在是各种争议的中心：

**安全**：默认给Agent完整宿主权限，沙盒是可选的。3月份4天内爆出9个CVE，最高CVSS评分9.9/10。虽然漏洞都已修补，但13.5万个暴露实例的影子还在。不过OpenClaw也在4月11日跟VirusTotal合作上线了技能安全扫描。

**成本**：Anthropic说Claude订阅本来就不设计给Agent用。"持续的推理循环、自动重试、工具链组合"让订阅模式不可持续。所以开了claw tax——5美元/月的Claude Pro用Agent每天能跑掉API计费下数百美元的token。对用户来说，这要么是50倍涨价，要么是被迫迁移到别的模型后端。

**归属**：Steinberger加入了OpenAI，创始人的去向和项目的独立性之间总有点微妙。OpenClaw基金会声称项目是社区所有，但OpenAI是赞助商之一，NVIDIA、Vercel也是。一个由大公司赞助的开源项目，能在多大程度上保持独立性？

## 它到底好在哪

抛开争议，OpenClaw的技术逻辑是真的有吸引力：

- **一个网关控制所有平台**——25+个消息渠道，一个Agent实例同时管理
- **语音唤醒和Talk Mode**——可以用ElevenLabs的TTS对话
- **ClawHub技能市场**——目前40000+个社区技能
- **模型无关**——Claude、GPT、Ollama本地模型都接，不锁死任何一家
- **NVIDIA NemoClaw**——企业级版本，专为GPU密集型任务优化

Andrej Karpathy说："Excellent reading. Love oracle and Claw."

有人评价："感觉就像20年前第一次用Linux而不是Windows。你真的在掌控一切。"

## 359K星之后

OpenClaw的故事不只是一个开源项目的增长曲线。它揭示了三件事：

第一，AI Agent的需求比模型厂商预期的来得更猛——用户不是在想"要不要用Agent"，而是在想"用什么框架让它跑最久最便宜"。claw tax的争议本质上是订阅制和Agent用量制之间的结构性矛盾。

第二，"封锁"从来不会消灭需求，只会把它推向竞争对手——OpenClaw在Anthropic封锁Claude OAuth后立刻加了OpenAI和Ollama支持，星数不降反升。

第三，开源社区的速度仍然碾压公司内部团队——一个20人的独立项目迭代速度超过了Anthropic和OpenAI的官方Agent产品。但这能维持多久是另一个问题。

---

*参考资料：Star-History《OpenClaw surpasses Linux》 | Winbuzzer《OpenClaw overtakes React》 | TechCrunch《Anthropic temporarily banned OpenClaw's creator》(2026.4.10) | The Decoder《Anthropic cuts off third-party tools》(2026.2.19)*

---

60天超越React十年的star，与其说OpenClaw有多好，不如说市场对"自己管自己的AI助手"这个需求有多饥渴。25+个平台、一个网关、模型随便换——这不是一个技术项目在赢，这是一整个使用场景在爆发。Anthropic每封一次Claude的口，OpenClaw就多涨一轮星，这个正反馈循环本身就是最好的故事。至于359K星到底能转化成多少稳定用户和商业价值，那是下一个阶段的问题。而现在这一刻，属于那个龙虾吉祥物。
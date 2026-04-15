# [开源万岁] 有人用Rust重写了Claude Code，还把泄漏的源码全塞进去了

![封面](https://platform.theverge.com/wp-content/uploads/sites/2/2025/08/STKB364_CLAUDE_D.jpg?quality=90&strip=all&crop=0%2C0%2C100%2C100&w=1200)

3月31日，Anthropic发布Claude Code 2.1.88更新。用户在安装包里发现了一个不该出现的东西——source map文件，里面装着超过51万行TypeScript源代码。

Anthropic的回应很淡定："一次发布打包事故，由人为错误导致，不是安全漏洞。没有客户数据或凭证泄露。"

但互联网不会等你淡定完。

## 52小时，5万 fork

泄漏发生后的52小时内，有人把代码复制到了GitHub上的instructkr/claw-code仓库。fork数迅速突破5万。开发者们像拿到新玩具一样翻箱倒柜，扒出的东西比大多数人预想的要多：

- **电子宠物"Tamagotchi"**——一个坐在输入框旁边、随你的编码行为做出反应的小家伙
- **"KAIROS"功能**——一个始终运行的后台Agent，暗示Claude Code正在走向"永远在线"
- **记忆架构**——会话管理、历史记录、上下文维护的完整数据流
- 还有Anthropic程序员留的一条坦率注释："这里的记忆化大幅增加了复杂度，我不确定它是否真正提升了性能。"

这是科技史上极为罕见的场景：一款商业AI工具的完整内部逻辑，以一种毫无戏剧性的方式——一个忘了剔除的source map——暴露在全世界的眼皮底下。

## 然后有人用Rust重写了它

泄漏的源码还没凉透，GitHub上就出现了一个新仓库：lorryjovens-hub/claude-code-rust。

项目声称这是Claude Code的"全量Rust重构版本"——性能提升2.5倍，体积减少97%，零依赖原生安全。

先看数据：

| 指标 | TypeScript版 | Rust版 | 提升 |
|------|-------------|--------|------|
| 启动时间 | 158ms | 63ms | 2.5x |
| 安装体积 | 164MB | 5MB | 97%减少 |
| 内存占用 | ~100MB+ | ~10MB | 10x |
| 配置查询 | 150ms | 6ms | 25x |
| Docker镜像 | ~600MB | ~20MB | 96%减少 |

仓库里甚至还有中文版README。项目结构完整，包含CLI、REPL、MCP服务器、插件系统、语音输入、SSH连接、内存管理——几乎原版Claude Code所有功能的Rust实现。它还默认接入DeepSeek的API，而非Anthropic的。

## 但这里面有几个问题需要冷静看

**第一，"97%的体积减少"这个数字怎么来的？**

TypeScript版164MB里，156MB是node_modules——这是Node.js生态的固有特征，不是TypeScript写得多烂。Rust版5MB是编译后的单一二进制文件，但当你要修改任何行为时，你需要重新编译。这是一个不公平但有效的对比——对终端用户来说，5MB确实比164MB好得多。

**第二，GitHub语言占比：TypeScript 97.5%，Rust 2.1%。**

你没看错。这个号称"Rust全量重写"的仓库，代码里97.5%是TypeScript。Rust只占了2.1%。仓库里有一个完整复制进来的`claude-code-main (2)`目录——这就是泄漏出来的原始TypeScript源码。所谓"重写"，很大程度上是把原版TypeScript代码和一套Rust骨架放在一起，再声称性能大幅提升。

**第三，1300+ star，550+ fork——但11个issue、2个PR。**

对于一个声称"完整重写"的项目，这个贡献比率极不正常。更像是大量围观群众在收藏，而非真正使用或开发。

**第四，性能基准来自项目自己的benchmark.ps1脚本。**

没有第三方验证，没有标准化的测试环境，没有可复现的对照实验。脚本跑出来的数字，当然是项目自己选择展示的数字。

## 真正值得关注的

抛开这些水分，这个项目折射出的是开发社区对AI编程工具的三个真实诉求：

**速度**——Claude Code的Node.js启动确实慢。任何在CI/CD管道里用过AI编程工具的人都知道，每秒都在烧钱。

**轻量**——164MB的node_modules在一个Docker容器里不算什么，但当你要同时跑50个实例时，5GB内存就不是开玩笑的事了。

**自主权**——项目默认接入DeepSeek而非Anthropic，这不仅是技术选择，更是一种态度——我不想被锁死在Claude的付费API上。

至于这个Rust版本身是不是一个真正的可用替代品？答案是：大概率还不能。但在AI编程工具这个日新月异的赛道上，它标记了一个方向——社区不满意现有工具的重量级运行时，而且愿意动手改变它。

---

*参考资料：The Verge《Claude Code leak exposes a Tamagotchi-style 'pet' and an always-on agent》(2026.3.31) | GitHub: lorryjovens-hub/claude-code-rust | Ars Technica《Entire Claude Code CLI source code leaks thanks to exposed map file》(2026.3.31)*

---

一个source map文件泄露了51万行代码，然后有人基于这些代码搞了个"Rust重写版"，里面97%还是TypeScript。这大概就是2026年AI开源社区的日常——一半是真诚的技术追求，一半是蹭热度的项目包装，而区分二者的唯一方法是去数代码行数。

但这个故事的弦外之音才是重点：AI编程工具的竞争正在从"谁的模型更强"转向"谁的工具链更轻更快"。Claude Code笨重的Node.js运行时不是Anthropic独有的问题——整个JavaScript生态的启动开销，在AI Agent需要每秒调用数十次的场景下，会成为真正的瓶颈。Rust版虽然现阶段更像个PPT项目，但它抓住了一个真实的痛点。谁能先把这个痛点解决掉，谁就能在AI编程的下一轮洗牌里占据生态位。
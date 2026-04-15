[开源万岁] 有人用Rust"重写"了Claude Code，97%的代码还是TypeScript

Claude Code 51万行源码泄漏，因为一个忘了删的source map文件。

然后GitHub上出现了claude-code-rust，号称"全量Rust重写"，启动快2.5倍，体积减少97%。

听起来很猛对吧？看一眼仓库语言占比：TypeScript 97.5%，Rust 2.1%。

所谓"重写"，就是把泄漏的TypeScript源码原样复制一份，套一层Rust骨架，跑自己写的benchmark出数据。1300个star，11个issue，2个PR——典型的围观型仓库。

但这个故事真正值得说的是：AI编程工具的竞争正在从"谁的模型强"转向"谁的工具链轻"。164MB的node_modules在CI/CD管道里每秒都在烧钱。痛点是真的，只是这个Rust版目前还是个PPT项目。

原文：
AI编程工具的下一轮洗牌，不比谁的模型聪明，比谁的运行时更轻。

#人工智能 #开源 #AI科技
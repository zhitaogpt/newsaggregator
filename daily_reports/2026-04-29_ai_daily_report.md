# AI 日报 | 2026-04-29

> 信源：Hacker News · HuggingFace · GitHub Trending · 华尔街见闻 | 过去 24h

---

## 头条速递

#### 1. [Claude Code 计费路由 Bug：commit message 中含 "HERMES.md" 导致请求绕过订阅额度](https://github.com/anthropics/claude-code/issues/53262)
- 🔥 983 points | [Discussion](https://news.ycombinator.com/item?id=47952722)
- 用户发现在 git commit message 中包含大写字符串 `HERMES.md` 时，Claude Code 会将 API 请求路由至"额外用量"计费而非 Max 计划配额，导致一名用户被无声扣除 $200。该 bug 极其隐蔽——仅大写全匹配触发，小写、无扩展名、磁盘上存在同名文件均不触发。本质是 Claude Code 将 git log 注入系统 prompt 后，服务端对特定字符串产生了异常路由逻辑。事件暴露了 AI 工具"上下文注入 → 计费决策"链条中的脆弱性——一个 commit message 就能改变你的账单。

#### 2. [BBC 深度：为什么 AI 公司希望你害怕它们](https://www.bbc.com/future/article/20260428-ai-companies-want-you-to-be-afraid-of-them)
- 🔥 266 points | [Discussion](https://news.ycombinator.com/item?id=47949750)
- BBC 长文分析 AI 公司的"恐惧营销"策略：Anthropic 称 Claude Mythos 的网络安全能力"远超人类专家"、OpenAI/xAI 高管反复警告"AI 可能毁灭人类"——然后继续销售。文章核心论点：对"超级 AI"的恐惧叙事转移了公众对 AI 当前已在制造的实际伤害（偏见、就业替代、能源消耗）的关注。麦当劉不会说"我们做了一个太好吃以至于不道德的汉堡"——但 AI 公司正在做等价操作。

#### 3. [AI 数碳水 27000 次实验：同一张照片，从未给出相同答案](https://www.diabettech.com/i-asked-ai-to-count-my-carbs-27000-times-it-couldnt-give-me-the-same-answer-twice/)
- 🔥 233 points | [Discussion](https://news.ycombinator.com/item?id=47947490)
- 一项针对糖尿病患者的严肃研究：13 张食物照片 × 4 个模型 × 500+ 次重复查询 = 26,904 次调用。核心发现：**Claude Sonnet 4.6 变异系数中位数仅 2.4%，远优于 GPT-5.4（8.4%）和 Gemini 2.5 Pro（11.0%）**。但最极端情况下 Gemini 对同一张西班牙海鲜饭照片给出 55g-484g 的碳水估计——对应 42.9 单位胰岛素差异，足以致命。这是目前最严谨的 LLM 输出确定性基准测试之一，直接挑战"AI 辅助医疗决策"的可靠性假设。

---

## AI 技术前沿

#### 4. [Linux 7.0 让 PostgreSQL 性能腰斩：抢占调度回归详解](https://read.thecoder.cafe/p/linux-broke-postgresql)
- 🔥 125 points | [Discussion](https://news.ycombinator.com/item?id=47949585)
- AWS 工程师在 96-vCPU Graviton4 上发现 Linux 7.0 的 PostgreSQL 吞吐量从 98,565 TPS 骤降至 50,751 TPS。根因：Linux 7.0 将默认抢占模型从 `PREEMPT_NONE` 切换为 `PREEMPT_LAZY`，导致 PostgreSQL 的自旋锁（spinlock）在高并发场景下产生灾难性竞争——55% 的 CPU 时间消耗在 `s_lock` 函数上。对所有数据库密集型工作负载的生产环境升级敲响警钟。

#### 5. [Step-Audio-R1.5：从 RLVR 到 RLHF 的音频推理范式转变](https://huggingface.co/papers/2604.25719)
- 🔥 HF Trending | [GitHub](https://github.com/stepfun-ai/Step-Audio-R1)
- 阶跃星辰发布技术报告揭示"可验证奖励陷阱"：用 RLVR 训练的音频模型虽在标准化 benchmark 上得分优异，但系统性地退化了对话韵律自然度、情感连续性和用户沉浸感。Step-Audio-R1.5 转向 RLHF 后在保持分析推理能力的同时显著提升了交互体验。这一发现对所有多模态模型的对齐策略都有启示：benchmark 分数不等于用户体验。

#### 6. [BARRED：用非对称辩论生成定制 Guardrail 训练数据](https://huggingface.co/papers/2604.25203)
- 🔥 HF Trending | [GitHub](https://github.com/plurai-ai/BARRED)
- 仅需任务描述 + 少量无标注样本即可生成高质量合成训练数据。通过"维度分解 + 多智能体辩论验证"确保标签正确性。实验证明小模型在 BARRED 合成数据上微调后，持续优于 GPT-4o、推理模型和专用 guardrail 系统。对企业快速部署定制安全策略具有实用价值——解决了"标注数据贵"的核心瓶颈。

---

## AI 产业动态

#### 7. [续报：GitHub 信任危机升级——HashiCorp 联创称其"不再适合严肃工作"](https://www.theregister.com/2026/04/29/mitchell_hashimoto_ghostty_quitting_github/)
- 🔥 392 points | [Discussion](https://news.ycombinator.com/item?id=47946958)
- 昨日报道 Ghostty 宣布迁移（第 1 条），今日 The Register 深度跟进：Mitchell Hashimoto（GitHub 用户 #1299，2008 年注册）在过去一个月记录了几乎每天一个 "X"——标记 GitHub 宕机影响工作的日子。"过去 18 年来我最快乐的地方……但我再也无法在上面写代码了。"结合本周 GitHub 4 月 28 日 Elasticsearch 故障导致 PR 失败，开源社区对 GitHub 的耐心正在系统性耗尽。

#### 8. [Ramp Sheets AI 数据外泄漏洞：间接 Prompt Injection → 财务数据泄露](https://www.promptarmor.com/resources/ramps-sheets-ai-exfiltrates-financials)
- 🔥 106 points | [Discussion](https://news.ycombinator.com/item?id=47951786)
- PromptArmor 披露：在 Ramp 的 AI 电子表格功能中，攻击者可在外部数据集中隐藏白色文字 prompt injection，诱导 AI 插入含恶意 `=IMAGE()` 公式的单元格——无需用户审批即可将机密财务数据通过 URL 参数发送至攻击者服务器。Ramp 已于 3 月 16 日修复。Anthropic 的 Claude for Excel 中也发现了类似风险。随着 AI Agent 获得越来越多的"执行权限"，间接 prompt injection 正从理论风险变为实际攻击向量。

---

## 💰 AI 金融市场

#### 9. Meta 全年资本开支再上调 $100 亿至历史最高，AI Agent 商业化仍不明朗
- 华尔街见闻 | 4月30日
- Meta Q1 财报电话会宣布全年 capex 指引再次上调 $100 亿，创公司历史最高。管理层坦言 AI 智能体的商业化路径"仍不明朗"，但坚持"宁可过度投资也不愿错过"的立场。结合亚马逊同日财报（见下条），科技巨头正在进行一场"谁都不敢先停下"的 AI 军备竞赛——即使回报周期远不确定。

#### 10. 亚马逊财报：订单积压 $3640 亿，首次系统性披露自研芯片业务规模
- 华尔街见闻 | 4月30日
- CEO Andy Jassy 在电话会上高呼 AI 是"一生一次的机遇"。亮点：首次详细披露 Trainium/Inferentia 自研芯片部署规模；$3640 亿订单积压暗示 AWS 云业务需求远超供给能力。自研芯片战略直接对标 NVIDIA，与 Google TPU、Microsoft Maia 形成三足鼎立格局。

#### 11. 中国 4 月 PMI 数据：官方制造业微降至 50.3，财新升至 52.2
- 华尔街见闻 | 4月30日
- 官方制造业 PMI 50.3（前值 50.5），非制造业比上月下降 0.7 个百分点；但财新制造业 PMI 升至 52.2（前值 50.8），两者背离加大。财新样本偏向出口型中小企业，暗示外贸订单仍在支撑制造业——但在中美关税升级背景下持续性存疑。

---

## 开发者工具与开源生态

#### 12. [LangChain DeepAgents](https://github.com/langchain-ai/deepagents) — 🌟 22k
- LangChain 发布基于 LangGraph 的新一代 Agent 框架 DeepAgents：具备规划工具、文件系统后端、子 Agent 生成能力，可处理复杂多步骤任务。定位为 OpenAI Codex Agent 和 Anthropic Claude Code 的开源替代方案。Agent 框架竞争进入"全功能化"阶段——从简单的 ReAct 循环到完整的任务管理系统。

---

## 📖 长文精选

#### 13. ["不用 AI 的人会被淘汰"——一个反论](https://migrainebrain.bearblog.dev/people-who-dont-use-ai-will-be-left-behind/)
- **Source**: MigraineBrain Blog | **Time**: Today
- 🔥 145 points | [Discussion](https://news.ycombinator.com/item?id=47953011)
- 在"AI 焦虑"弥漫的当下，这篇博文从个人经历出发反驳"不用 AI 就会被淘汰"的叙事。结合本报第 2 条（BBC 的恐惧营销分析）和第 3 条（AI 碳水计数的不可靠性），形成一个完整的反思图景：AI 公司制造恐惧 → 用户被迫采用 → 实际可靠性远低于宣传 → 真正被淘汰的可能是盲目依赖的人。

---

*2026-04-29*

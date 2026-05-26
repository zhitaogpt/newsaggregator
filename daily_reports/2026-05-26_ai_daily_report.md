# AI 日报 | 2026-05-26

> 信源：Hacker News · HuggingFace Papers · Latent Space · Anthropic · 华尔街见闻 · Religion News · Business Insider | 过去 24h

## 今日摘要

- 教皇 Leo XIV 首份通谕点名"少数公司垄断 AI"，Anthropic 联创公开回应——AI 治理叙事进入宗教/人文第三轨
- Claude 首次以独立研究者身份获 Apple CVE 致谢，AI 漏洞挖掘从精英特权变为 API Key 即可触达
- Uber、Anthropic 计量化、华尔街见闻三方共振：AI ROI 叙事退潮，2026 下半年算力 vs 应用估值分歧加剧

---

## 头条速递

#### 1. [教皇 Leo XIV 发布首份通谕《Magnifica Humanitas》：AI 必须服务人类，而非少数权贵](https://religionnews.com/2026/05/25/in-his-first-encyclical-pope-leo-xiv-says-ai-must-serve-humanity-not-the-powerful-few/)
- 🔥 333 + 163 + 71 + 13 points（HN 当日四帖前排） | [Anthropic 联合创始人 Chris Olah 公开回应](https://www.anthropic.com/news/chris-olah-pope-leo-encyclical)
- 教皇 Leo XIV 在登基后首份正式通谕中将"由少数公司运行的不透明 AI"列为"新型去人性化（New Forms of Dehumanization）"风险，明确呼吁"解除（disarm）AI 的武器化倾向"，并引用《指环王》中甘道夫的隐喻。**Anthropic 联合创始人 Chris Olah 罕见以个人名义发表回应**，承认通谕的核心论点与可解释性（interpretability）研究的目标一致——这是顶级 AI 实验室第一次公开承认外部伦理权威的合法性。**含义**：AI 治理叙事正在从"技术专家自我监管 vs 政府监管"的二元对立，转向"宗教/人文传统介入"的第三轨。这与下文 #3 Uber COO 的"AI ROI 质疑"形成奇异的合奏——AI 公司刚刚发现自己同时面临**经济合理性**和**道德合法性**的双重审查。

#### 2. [CVE-2026-28952：Claude 在 macOS 26.5 内核中发现真实漏洞，AI 安全研究迈过临界点](https://support.apple.com/en-us/127115)
- 🔥 62 points | [Discussion](https://news.ycombinator.com/item?id=48270000)
- Apple 在 macOS Tahoe 26.5 安全公告中**首次明确署名 Claude 为 CVE 发现者**——这是大型操作系统厂商第一次把 AI 模型作为漏洞研究的"独立署名研究者"。结合下文 #4 Anthropic 计划公开发布的 Mythos 类模型，攻防力量对比正在重写：**过去发现 0day 是少数顶尖研究员的特权，现在每个有 API Key 的开发者都可能产出 CVE**。Apple 此次同一公告中署名了 7 位人类研究员 + 1 个 AI 模型——这种"AI 与人类并列致谢"的范式如果在 Google/Microsoft/Linux 跟进，会彻底改变漏洞悬赏（bug bounty）市场的定价机制。

#### 3. [Uber COO：AI tokenmaxxing 越来越难找到 ROI 理由，CTO 已"打爆 2026 Claude Code 预算"](https://www.businessinsider.com/uber-coo-andrew-macdonald-ai-token-spending-harder-justify-2026-5)
- 🔥 190 points | Business Insider
- Uber 运营总裁 Andrew Macdonald 在最新访谈中承认 AI 投入正面临"头脑爆炸时刻"——CTO Praveen Neppalli Naga 此前透露 Uber 已在 2026 年 4 月前就花光了全年 Claude Code 预算。Macdonald 直言"和资深工程负责人沟通后发现，**更高的 token 用量并未带来等比例的产出提升**"，正考虑权衡 token 支出与人员编制的关系。**与前文 #1 教皇通谕、下文 #8 高盛 CEO "AI 工作末日被夸大"形成三重共振**：在企业级买家侧，"无脑 AI 化"叙事正在退潮，2026 下半年财报季有望出现第一波**AI 预算回撤**信号。

---

## AI 技术前沿

#### 4. [Anthropic 计划向公众释放 Mythos 级漏洞挖掘模型，"Project Glasswing"扩容](https://www.theregister.com/security/2026/05/25/anthropic-to-release-mythos-class-models-to-the-public/5245596)
- 🔥 13 points | The Register
- Anthropic 宣布将在解决"防护栏"后向公众发布与 Mythos 性能相当的漏洞挖掘模型。Mythos 当前通过"Project Glasswing"仅对**精选企业与政府机构**开放，参与方反馈是"找到的 bug 多到无法修完"。**日本政府已下令全国安全大检查、印度监管部门强制金融机构紧急打补丁**——这是 AI 模型第一次**直接触发主权国家级别的应急响应**。Anthropic 此次为何此时松口？结合前文 #2 Claude 找出 macOS 内核漏洞、#3 客户对 AI ROI 的质疑，Anthropic 需要**用一个"杀手级垂直应用"重新讲清楚 AI 的不可替代价值**——网络安全是少数能用"防止重大事故"作为 KPI 直接证明价值的赛道。

#### 5. [HF Papers #1 of Day：SMART——让单向量 embedding 模型解锁多向量能力，无需重训](https://huggingface.co/papers/2605.24938)
- 🔥 Trending #1 | 5 月 24 日上线
- 论文证明：**标准对比训练在 pooled embedding 上已经隐式塑造了前层隐藏状态的检索几何结构**——也就是说现有 single-vector 模型其实"自带"多向量能力，只是被你的池化操作丢掉了。SMART 框架在推理阶段对冻结的隐藏状态做 late-interaction，作为"插即用升级"在多模态检索任务上**无需训练即达到 SOTA**。**对 RAG 工程师的直接意义**：你今天用的 OpenAI/Cohere/Voyage 三家 embedding 模型理论上都能用 SMART 这套推理增强免费提升一个档位——这是 2026 年第一篇真正实用、可立即落地的"零训练 RAG 升级"论文。

---

## AI 产业动态

#### 6. [挪威国家图书馆用 2PB 华为闪存训练挪威语主权 LLM，欧洲"去美国化"算力出现实证](https://www.blocksandfiles.com/flash/2026/05/22/norways-2-petabytes-of-huawei-flash-storage-and-llm-training/5244910)
- 🔥 156 points | Blocks & Files
- 挪威国家图书馆使用 **2 PB 华为 OceanStor Dorado 闪存阵列**为挪威语主权 LLM 提供训练数据管道——这是欧洲一级 NATO 国家公共部门**首次公开**在 AI 训练基础设施上选用华为存储。挪威 IT 平台负责人 Marius Husnes 给出的理由是"没有商业 LLM 厂商在做挪威语模型"。**含义**：北约国家政府用华为做 AI 基建在去年还是政治禁区，今年已经是公开 case study——叠加前文 #1 教皇通谕对"少数美国公司垄断 AI"的批评、加上前几日（5/25 报告）的华为"韬定律"，**欧洲 AI 主权叙事正在为非美算力打开实质性窗口期**，对 NVIDIA/Dell/Pure Storage 等美国供应链不利。

#### 7. [Latent Space 一周观察：Codex 上升，Claude 开始计量化使用；Anthropic 同比增长 10 倍](https://www.latent.space/p/ainews-codex-rises-claude-meters)
- **Source**: Latent Space AINews | **Time**: 2026-05-21
- Latent Space 本周三个数据点：(a) OpenAI 的 Codex 用量曲线开始反超 Claude Code；(b) Anthropic 开始对 Claude Code 做**计量化使用控制（programmatic usage metering）**——这是回应"客户打爆预算"问题的工程响应；(c) Anthropic 整体收入仍以**同比 10 倍**速度增长，而行业大多数公司在裁员。**与前文 #3 Uber 案例直接对仗**：Anthropic 计量化是供给侧的诚实——承认 token 经济学正在重定价；同时 10 倍增长意味着即便"客户开始算账"，整体增量仍远超回撤。

---

## 💰 AI 金融市场

#### 8. [华尔街见闻独家：决定 AI 牛市的关键变量是什么？](https://wallstreetcn.com/articles/3773111)
- **Source**: 华尔街见闻 | **Time**: 2026-05-26 09:24
- 华尔街见闻今早发布的策略文章直指 AI 牛市的核心变量。**结合下文 #9 半导体股集体涨 15%、与前文 #3 Uber 质疑 ROI、#7 Anthropic 计量化**——市场叙事正在分化：买方相信"token 经济学已经验证 → 算力链确定性最高"，卖方担忧"前端应用 ROI 撑不起算力溢价"。这是 2026 下半年 AI 板块**最关键的认知分歧**——决定下一轮是"算力一枝独秀"还是"应用-算力共振修复"。

#### 9. [A 股 5/26 早盘：华虹、中芯国际涨 15%，宇树机器人概念走强，恒生科技涨 1.9%](https://wallstreetcn.com/articles/3773113)
- **Source**: 华尔街见闻 | **Time**: 2026-05-26 09:27
- A 股集体低开后半导体强势回暖：**华虹半导体、中芯国际盘中涨幅 15%**，宇树机器人概念走强，恒生科技指数涨 1.9%。**接续前一日（5/25 报告）寒武纪破 9000 亿的产业链狂欢**，但今日资金从"AI 算力核心"扩散至"代工双雄 + 机器人"两条新主线——前者受益于美国出口管制下的国产替代加速，后者对接前文 #6 欧洲非美算力链以及全球具身智能投资热。**关键观察**：创业板今早依然弱于主板，意味着资金仍以"硬件+周期 hybrid"为主，纯成长股待破局。

#### 10. [黄仁勋：奋斗是因为"早年艰辛"，希望"死在工作岗位上"](https://wallstreetcn.com/charts/41959125)
- **Source**: 华尔街见闻 | **Time**: 2026-05-26 09:25
- 黄仁勋在最新公开访谈中表态"希望死在工作岗位上"，将自己的奋斗驱动力归因于"早年艰辛"。**为何这条值得入选**：NVIDIA 创始人的个人发言历来被市场视作"对未来 AI 算力周期持续性的隐含信号"——他选择在此时强调"长期主义工作伦理"，与前文 #3 Uber 的 AI ROI 质疑、#8 华尔街见闻的牛市拐点讨论形成微妙时机错位，可能是在为投资者对算力 Capex 持续性的疑虑提前定调。

---

## 📖 长文精选

#### 11. [Latent Space：所有 Model Labs 都正在变成 Agent Labs](https://www.latent.space/p/ainews-all-model-labs-are-now-agent)
- **Source**: Latent Space AINews | **Time**: 2026-05-23（昨日报告头条延续追踪）
- *续报*：在 5/25 日报头条提及 OpenAI 转向 Agent 公司之后，本周 Latent Space 进一步给出三家 AI 基建独角兽——**Exa（搜索 API）、Modal（GPU 云）、TurboPuffer（向量数据库）**——的估值跃迁数据，以及 Daytona 和 Railway 两位创始人对"Agent-native 云"的展望访谈。**关键判断**：与前文 #4 Anthropic 把 Mythos 推向公众、#7 Codex 反超 Claude Code 形成完整证据链——**2026 Q3-Q4 的产品端竞争主战场已确定为"Agent 工作完成率"**，纯模型 API 公司会在年底前出现一次估值回归，而 Agent 基础设施公司会接力成为下一轮叙事。

---

*2026-05-26*

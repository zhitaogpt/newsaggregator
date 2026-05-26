# AI 日报 | 2026-04-28

> 信源：Hacker News · HuggingFace · Latent Space · 华尔街见闻 · 36氪 | 过去 24h

---

## 头条速递

#### 1. [微软与 OpenAI 终结独家收入分成协议](https://www.bloomberg.com/news/articles/2026-04-27/microsoft-to-stop-sharing-revenue-with-main-ai-partner-openai)
- 🔥 753 points | [Discussion](https://news.ycombinator.com/item?id=47921248)
- 微软将停止与 OpenAI 的收入分成，双方多年独家合作关系迎来根本性转变。OpenAI 同步发文阐述"partnership 下一阶段"。结合第 3 条 Copilot 按用量计费，AI 行业正从订阅制全面转向"按 token 付费"模式。

#### 2. [中国叫停 Meta 20 亿美元收购 Manus](https://www.cnbc.com/2026/04/27/meta-manus-china-blocks-acquisition-ai-startup.html)
- 🔥 302 points | [Discussion](https://news.ycombinator.com/item?id=47920315)
- 国家发改委要求 Meta 撤回对新加坡 AI Agent 公司 Manus 的收购。Manus 从中国迁至新加坡，ARR 已破 1 亿美元，被称为"下一个 DeepSeek"。此举打击"新加坡洗白"模式，对试图离岸规避中美审查的 AI 创始人和 VC 震动极大。

#### 3. [GitHub Copilot 转向按用量计费](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/)
- 🔥 545 points | [Discussion](https://news.ycombinator.com/item?id=47923357)
- 6月1日起，Copilot 所有计划将转向基于 token 消耗的 "GitHub AI Credits" 计费。代码补全不消耗 Credits，但 Agent 式长会话成本将显著增加。基础价格不变（Pro $10/月），但取消 fallback 降级体验。AI 编程工具"无限订阅"时代终结。

---

## AI 技术前沿

#### 4. [SIREN：从 LLM 内部表征检测有害内容，参数量仅需 1/250](https://huggingface.co/papers/2604.18519)
- 🔥 +13 | [GitHub](https://github.com/CSSLab/SIREN) | 📅 2026-04-28
- 通过识别 LLM 内部各层"安全神经元"并自适应加权，构建轻量级有害内容检测器。参数量仅为现有 guard model 的 1/250，却显著超越开源 SOTA，支持实时流式检测且无需修改底层模型。LLM 内部安全信号正成为比外部过滤更高效的范式。

#### 5. [Decoupled DiLoCo：Google 分布式训练新架构](https://deepmind.google/blog/decoupled-diloco/)
- 🔥 44 points | [Discussion](https://news.ycombinator.com/item?id=47924181) | 📅 Today
- 将大型训练拆分为异步"计算岛"，单岛故障不中断其余训练，故障节点恢复后自动重新整合。在 Gemma 4 上验证，解决了全球分布式训练的核心痛点——跨数据中心同步的高延迟与脆弱性。

---

## AI 产业动态

#### 6. [4TB 语音数据从 Mercor 4 万名 AI 标注员处被盗](https://app.oravys.com/blog/mercor-breach-2026)
- 🔥 441 points | [Discussion](https://news.ycombinator.com/item?id=47919630)
- Lapsus$ 泄露约 4TB 数据，包含 4 万人语音样本+身份证+自拍。15 秒干净语音即可克隆声纹，泄露数据平均每人 2-5 分钟录音室级音频。5 起诉讼已提起，指控公司未明确告知语音将作为生物标识符永久保存。AI 数据供应链安全到了不可忽视的临界点。

#### 7. [Mistral 靠"不做美国公司"打造 140 亿美元 AI 帝国](https://www.forbes.com/sites/iainmartin/2026/04/16/how-frances-mistral-built-a-14-billion-ai-empire-by-not-being-american/)
- 🔥 203 points | [Discussion](https://news.ycombinator.com/item?id=47919725)
- Forbes 深度报道：Mistral 利用 GDPR 合规优势、法国政府支持、欧盟 AI 监管窗口期，从 7 人团队成长为 $14B 估值。与美国 AI 公司面临出口管制形成对照，"非美路线"为全球 AI 公司提供了另一种范式。

#### 8. [Dirac：开源 Agent 登顶 TerminalBench 2.0](https://github.com/dirac-run/dirac)
- 🔥 303 points | [Discussion](https://news.ycombinator.com/item?id=47920787)
- 在 Gemini-3-flash-preview 上以 65.2% 超越 Google 官方基线（47.6%）和闭源 Junie CLI（64.3%）。核心：Hash Anchored 编辑+大规模并行+AST 操控，API 成本降 50-80%，不使用 MCP。

---

## 💰 AI 金融市场

#### 9. [OpenAI 用户和营收双双未达标](https://wallstreetcn.com/articles/3771064)
- 华尔街见闻 | 4月28日
- CFO 警告"还没准备好上市"，或难履行算力采购合同。与第 1 条微软终结收入分成形成闭环——增长放缓+成本压力加剧，AI 产业链商业模式面临严峻考验。

#### 10. [AI 完成任务的成本已可能超过人工](https://www.axios.com/2026/04/26/ai-cost-human-workers)
- 🔥 85 points | [Discussion](https://news.ycombinator.com/item?id=47918009)
- Axios 报道：Agent 式 AI 使用量激增下，AI 完成任务成本已可能超过雇佣人类。与第 3 条 Copilot 按用量计费、第 9 条 OpenAI 营收未达标形成完整叙事链——AI 经济性优势可能仅存在于高附加值场景。

---

## 开发者工具与开源生态

#### 11. [Tendril：能自建工具的自扩展 Agent](https://github.com/serverless-dna/tendril) — 🌟 127 | [Utilyze：比 nvtop 更准的 GPU 监控](https://www.systalyze.com/utilyze)
- 🔥 70 + 86 points
- **Tendril**：仅 3 个引导工具，Agent 检查能力注册表→不存在则编写并注册新工具→执行，每次会话比上次更聪明。**Utilyze**：揭示 nvidia-smi/nvtop 报告的 100% GPU 利用率下真实计算可能仅 1%，对优化 AI 训练成本有直接价值。

---

## 📖 长文精选

#### 12. [在十小时航班上离线运行本地 LLM](https://deploy.live/blog/running-local-llms-offline-on-a-ten-hour-flight/)
- 🔥 111 points | [Discussion](https://news.ycombinator.com/item?id=47921064)
- MacBook Pro M5 Max（128GB）+ Gemma 4 31B / Qwen 4.6 36B，10 小时处理约 400 万 token，完成了一个账单分析工具。三大瓶颈：功率（1%/分钟）、散热（70-80W 机身烫手）、上下文（超 100k token 后吞吐骤降）。对"本地 AI"能力边界的真实测试，比任何基准更有说服力。

---

*2026-04-28*
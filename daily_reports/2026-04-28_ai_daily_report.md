# AI 日报 | 2026-04-28

> 信源：Hacker News · HuggingFace · GitHub Trending · Google Search · 华尔街见闻 · 36氪 | 过去 24h

---

## 头条速递

#### 1. [Ghostty 宣布离开 GitHub](https://mitchellh.com/writing/ghostty-leaving-github)
- 🔥 1682 points | [Discussion](https://news.ycombinator.com/item?id=47939320)
- HashiCorp 创始人 Mitchell Hashimoto 宣布其终端模拟器 Ghostty（52k stars）将迁移出 GitHub。理由涉及 GitHub 服务稳定性下降、AI 功能侵蚀开发体验、以及对开源项目的态度转变。结合今日另外几条 GitHub 相关新闻（RCE 漏洞、Actions 安全风险、Copilot 收费变更、可用性事故），GitHub 正面临开源社区前所未有的信任危机。BookStack 同日宣布迁至 Codeberg（第 10 条），或开启开源项目"去 GitHub 化"浪潮。

#### 2. [Google 与五角大楼签署机密 AI 协议](https://www.theverge.com/ai-artificial-intelligence/919494/google-pentagon-classified-ai-deal)
- 🔥 270 points | [Discussion](https://news.ycombinator.com/item?id=47938417)
- Google 签署协议允许美国国防部将 Gemini 模型用于"任何合法政府目的"的机密工作。此前 OpenAI 和 xAI 已签署类似协议。2025 年五角大楼与各主要 AI 实验室签署的合同总额均达 $2 亿级别。AI 军事化已从争议话题变为行业共识——唯一的问题是谁能拿到合同，而不是该不该做。

#### 3. [续报：OpenAI 模型正式上线 AWS Bedrock，微软-OpenAI 独家协议彻底终结](https://stratechery.com/2026/an-interview-with-openai-ceo-sam-altman-and-aws-ceo-matt-garman-about-bedrock-managed-agents/)
- 🔥 179 points | [Discussion](https://news.ycombinator.com/item?id=47939320)
- 昨日报道微软与 OpenAI 终结收入分成，今日后续：OpenAI 模型已正式在 AWS Bedrock 上线（含 Codex 和全新 Managed Agents 产品），微软授予非独家许可。Ben Thompson 深度采访双方 CEO：Altman 坦言"Azure 独家限制了我们触达企业客户"，Garman 则称这是"AWS 客户最希望得到的"。Anthropic 此前在多云策略上的领先优势被直接削弱——AI 模型分发正快速走向"水电煤"化。

---

## AI 技术前沿

#### 4. [AISLE 用 AI 分析器发现医疗软件 38 个 CVE 漏洞](https://aisle.com/blog/aisle-discovers-38-critical-security-vulnerabilities-in-healthcare-software-used-by-100000-providers)
- 🔥 166 points | [Discussion](https://news.ycombinator.com/item?id=47936347)
- AI 安全公司 AISLE 在 2026 Q1 用自动化分析引擎对 OpenEMR（10 万+ 医疗机构使用，覆盖 2 亿患者）发现 38 个 CVE，包括 2 个 CVSS 10.0 的 SQL 注入漏洞。对比 2018 年人类团队审计发现的 23 个漏洞，效率提升显著。此前该引擎在 OpenSSL 发现 12 个零日漏洞。AI 在安全审计领域正从辅助角色变为核心生产力。

#### 5. [Programming with Data：用软件工程方法论驱动 LLM 训练数据修复](https://huggingface.co/papers/2604.24819)
- 🔥 Trending | [GitHub](https://github.com/OpenRaiser/ProDa) | 📅 2026-04-29
- 将训练数据视为"源代码"，模型训练视为"编译"，benchmark 视为"单元测试"——当模型在特定概念上失败时，追溯到训练数据中的缺陷并定向修复。跨 16 个学科验证，每轮修复都带来一致提升且不损害通用能力。这是 LLM 数据工程从"加更多数据"到"精准调试"的范式转变。

#### 6. [Recursive Multi-Agent Systems：将递归缩放原则推广到多智能体](https://huggingface.co/papers/2604.25917)
- 🔥 +6 | [GitHub](https://github.com/RecursiveMAS/RecursiveMAS) | 📅 2026-04-29
- RecursiveMAS 使多个 Agent 通过迭代潜空间计算进行协作推理，兼顾效率与准确性。Multi-Agent 系统从"任务分配"向"协作推理"演进，为 Agent 集群提供了新的 scaling 路径。

---

## AI 产业动态

#### 7. [Anthropic 加入 Blender ��金会成为企业赞助人](https://www.blender.org/press/anthropic-joins-the-blender-development-fund-as-corporate-patron/)
- 🔥 240 points | [Discussion](https://news.ycombinator.com/item?id=47936370)
- Anthropic 以 Corporate Patron 级别加入 Blender 基金会，资金专用于 Blender 核心开发。AI 公司赞助 3D 开源工具背后的逻辑：训练多模态模型需要高质量 3D 数据和渲染管线，Blender 是最大的开源 3D 数据生成器。同时也是对开源社区的一种"善意投资"——在 AI 公司与开源社区关系日趋紧张的当下（见第 1 条），Anthropic 选择了不同的姿态。

#### 8. [OpenAI CEO 的身份验证公司 World 因虚假合作声明被曝光](https://www.vice.com/en/article/openai-ceo-identity-verification-company-fake-bruno-mars-partnership-mistaken-identity/)
- 🔥 279 points | [Discussion](https://news.ycombinator.com/item?id=47938417)
- Sam Altman 的 World（前 Worldcoin）宣布与 Bruno Mars 合作进行身份验证，被 Vice 证实为虚假合作。该公司在全球推广虹膜扫描面临多国监管审查，此事件进一步损害其公信力。AI 领域"先造势后兑现"的文化开始遭到反噬。

#### 9. [AGENTS.md 文件质量研究：好的等于升级模型，差的不如没有](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files)
- 🔥 103 points | [Discussion](https://news.ycombinator.com/item?id=47938417)
- Augment Code 发布内部研究：最好的 AGENTS.md 文件相当于从 Haiku 升级到 Opus 的代码生成质量提升，但同一文件在简单任务 +25% 的同时可能在复杂任务 -30%。核心发现：100-150 行 + 按需引用的参考文件是最佳范式，超过后效果反转。对 AI 编程工具的"提示工程"正在变成一门实证科学。

---

## 💰 AI 金融市场

#### 10. [OpenAI"鬼故事"重创美股，美债市场"没慌"](https://wallstreetcn.com/articles/3771182)
- 华尔街见闻 | 4月29日
- OpenAI 利空叠加美伊局势悬而未决，美股美债齐跌，半导体板块回调。但债市并未出现恐慌性抛售，暗示市场将 OpenAI 风险视为行业个体事件而非系统性风险。WTI 原油突破 $100，布伦特三周来首次突破 $110。

#### 11. [希捷季报大超预期，2027 年产能几乎卖光](https://wallstreetcn.com/articles/3771186)
- 华尔街见闻 | 4月29日
- "硬盘巨头"宣布进入"结构性增长新时代"，CEO 称 AI 数据中心对大容量存储的需求已将 2027 年产能锁定。AI 训练和推理产生的数据量正在创造存储行业的超级周期——算力之外，"存力"成为新瓶颈。

---

## 开发者工具与开源生态

#### 12. [VibeVoice：微软开源前沿语音 AI](https://github.com/microsoft/VibeVoice) — 🌟 33.5k
- 🔥 320 points | [Discussion](https://news.ycombinator.com/item?id=47939320)
- 微软开源的全栈语音 AI 框架，覆盖 TTS（60 分钟多人播客级）、ASR（单 pass 处理 60 分钟音频）、语音克隆。目前 GitHub 33.5k stars，在 HN 再次热门或因近期新功能更新。开源语音 AI 工具链趋于成熟，门槛持续下降。

#### 13. [BookStack 正式迁移至 Codeberg](https://github.com/BookStackApp/BookStack/issues/4551)
- 🔥 77 points
- 开源知识管理平台 BookStack（18.7k stars）正式完成从 GitHub 到 Codeberg 的迁移。核心动机：GitHub 将公开代码用于 AI 训练、UX 被 AI 功能侵蚀、向"AI 平台"转型偏离开源使命。与 Ghostty（第 1 条）形成呼应，开源社区正在用脚投票。

---

## 📖 长文精选

#### 14. [AI 的经济学没有意义](https://www.wheresyoured.at/ais-economics-dont-make-sense/)
- **Source**: Ed Zitron / Where's Your Ed At | **Time**: 2026-04-28
- 🔥 192 points | [Discussion](https://news.ycombinator.com/item?id=47939320)
- Ed Zitron 深度分析 AI 行业经济学困境：GitHub Copilot 转向按用量计费本质是"无法继续补贴用户"，OpenAI 与微软终结独家是"增长故事难以为继"。文章核心论点：Agent 式 AI 使用量激增但收入未成比例增长，AI 公司面临"越用越亏"的结构性矛盾。值得完整阅读——对 AI 泡沫论述目前最数据翔实的版本之一。

#### 15. [GitHub 之前：开源协作的前世今生](https://lucumr.pocoo.org/2026/4/28/before-github/)
- **Source**: Armin Ronacher (Flask 作者) | **Time**: 2026-04-28
- 🔥 262 points
- 在 GitHub 遭遇信任危机之际，Flask 创建者回顾了 SourceForge、Google Code、Bitbucket 时代的开源协作方式。核心洞察：GitHub 的成功不在于 Git 托管，而在于 Pull Request 发明了一种"低门槛贡献"的社交协议。下一代平台需要保留这种社交创新，而不仅仅是去中心化存储。

---

*2026-04-28*

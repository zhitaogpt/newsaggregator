# newsaggregator · 韬见 AI

聚合 AI 技术浪潮 + 资本市场变化，每日生成结构化日报并发布到公众号「韬见 AI」。

## 仓库结构

| 路径 | 说明 |
|---|---|
| `.claude/skills/ai-daily-report/` | 日报撰写规范（必含"## 今日摘要"区块） |
| `.claude/skills/wechat-article-publisher/` | wx.limyai 公众号发布 API 封装 |
| `scripts/wechat_render/render.py` | 自研 markdown → 微信兼容内联 HTML 转换器 |
| `scripts/wechat_render/cover_render.py` | 自动生成 900×384 日报封面（品牌一致） |
| `daily_reports/YYYY-MM-DD_ai_daily_report.md` | 历史日报存档 |
| `brand_assets/taojian_avatar/` | 公众号头像（韬见 AI · 瞳孔光圈方向） |
| `brand_assets/wechat_render/` | 渲染输出（HTML + 封面 PNG），同时充当 GitHub 图床 |

## 端到端流程

```bash
# 1. 渲染日报 HTML（注入封面）
python3 scripts/wechat_render/cover_render.py daily_reports/2026-05-26_ai_daily_report.md brand_assets/wechat_render/cover_0526.png
python3 scripts/wechat_render/render.py daily_reports/2026-05-26_ai_daily_report.md brand_assets/wechat_render/v6_0526.html

# 2. 推送草稿（cover 走 GitHub raw URL）
python3 .claude/skills/wechat-article-publisher/scripts/wechat_api.py publish \
  --appid $WECHAT_APPID \
  --html brand_assets/wechat_render/v6_0526.html \
  --cover "https://raw.githubusercontent.com/zhitaogpt/newsaggregator/main/brand_assets/wechat_render/cover_0526.png" \
  --summary "今日摘要 3 条精炼版本"
```

## 配置

复制 `.env.example` 到 `.env`，填入：
- `WECHAT_APPID` — 公众号 AppID
- `WECHAT_API_KEY` — wx.limyai 平台 API Key

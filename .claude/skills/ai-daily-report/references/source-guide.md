# Source Selection Guide

## Primary Sources (Always Fetch)

| Source Key | Strength | What to Look For |
|---|---|---|
| `hackernews` | Tech community signal, high discussion quality | Items with 100+ points; rich comment threads |
| `huggingface` | Research frontier, trending papers | Trending papers with high upvotes; novel architectures |
| `github` | Open source ecosystem pulse | Star velocity (not just total); AI/ML repos |
| `latentspace` | AI industry deep analysis, insider perspective | Newsletter digests; podcast transcripts |
| `bensbites` | AI product ecosystem, funding news | Product launches; funding rounds; market signals |

## Secondary Sources (Fetch for Depth)

| Source Key | Strength | When to Use |
|---|---|---|
| `wallstreetcn` | China finance + AI market data | Always — for AI 金融市场 section |
| `36kr` | China tech industry moves | Always — for China AI coverage |
| `essays` | Long-form insight (aggregates paulgraham, farnamstreet, scottyoung, etc.) | Always — for 长文精选 section |
| `podcasts` | Deep conversations (aggregates lexfridman, latentspace, 80000hours) | When essays alone are thin |
| `producthunt` | New AI product launches | When product section needs items |

## Supplementary Sources (Use Google Search)

For data NOT covered by fetch_news.py sources:
- AI stock prices and movements (NVDA, AMD, INTC, MSFT, GOOG)
- IPO timelines and valuations
- Funding round details
- China AI chip companies (寒武纪, 壁仞, 燧原, 百度昆仑)
- Global AI chip market data

Search patterns:
```
"AI stocks market {today's date}"
"AI funding round 2026"
"AI芯片 市场 {今日日期}"
"OpenAI Anthropic ARR revenue 2026"
```

## Source Quality Tiers

When items from multiple sources cover the same story, prefer:
1. Primary source (company blog, official announcement)
2. Quanta Magazine, TechCrunch, The Information (quality journalism)
3. Newsletter analysis (Latent Space, Ben's Bites)
4. Community discussion (HN, GitHub)
5. Aggregator coverage (36Kr, 华尔街见闻)

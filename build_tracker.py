#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json

CASES = {
  "binance_20261029": {
    "id": "binance_20261029",
    "name": "Binance · 2026-10-29 热钱包史上最大盗窃",
    "exchange": "Binance",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 6430000000,
    "lossLabel": "约 $63–64.3 亿（历史最大）",
    "summary": "攻击者经虚假招聘面试、恶意软件、篡改开发工具与内部 AI 工具等路径潜伏数月，渗透钱包工程环境并滥用热钱包签名基础设施（含 EIP-7702）。10/29 起多链抽干热钱包，公开口径约 $63–63.4 亿。FBI 归因朝鲜。币安承诺 SAFU/自有资金全额覆盖；约 $28.5–30 亿被冻结/拦截；约 10/31 称补足约 98% 受影响资产。",
    "kpis": [
      {"n": "~$63–63.4亿", "l": "被盗规模（历史最大）"},
      {"n": "~$28.5–30亿", "l": "已冻结/拦截"},
      {"n": "~98%", "l": "受影响资产已补足口径"},
      {"n": "FBI", "l": "归因朝鲜相关"},
      {"n": "EIP-7702", "l": "热钱包执行权限被滥用"},
      {"n": "假面试", "l": "社工+恶意软件入口"},
    ],
    "statuses": [
      ["事件状态", "已遏制、补仓基本完成口径", "提币曾暂停后恢复", "warn"],
      ["用户赔付", "承诺全额覆盖", "SAFU+公司资金", "ok"],
      ["根因", "供应链/社工→签名基础设施", "非单纯私钥拷贝", "bad"],
      ["冻结", "约$28.5–30亿", "稳定币与拦截", "ok"],
      ["归因", "FBI归因朝鲜", "媒体简报公开", "info"],
    ],
    "timeline": [
      {"t": "2026-06", "d": "钱包开发者安装被篡改工具；换机后团队仍暴露"},
      {"t": "2026-09", "d": "假招聘面试诱导下载含恶意软件编码任务"},
      {"t": "10-20", "d": "借被控机器与内部AI工具入侵钱包工程师电脑"},
      {"t": "10-29 ~20:05 UTC", "d": "多链热钱包开始外流（含大量XRP/BTC/SOL等）"},
      {"t": "10-29当晚", "d": "暂停提币；EIP-7702恶意授权仍可继续抽款"},
      {"t": "10-30 00:10 UTC", "d": "官方称遏制签名侧外流并撤销授权"},
      {"t": "10-31→11-03", "d": "冻结约$28.5亿+；补仓约98%；假面试细节与FBI归因公开"},
    ],
    "fundFlow": [
      ["被盗", "多链热钱包", "含BTC、XRP、SOL、ETH侧EIP-7702抽款等"],
      ["已冻结", "约$28.5–30亿", "发行方冻结+拦截口径"],
      ["未冻资产", "兑ETH等并跨链", "脚本持续洗钱"],
      ["平台补仓", "公司资金+SAFU", "用户账面承诺不受损"],
    ],
    "links": [
      ["Elliptic分析", "https://www.elliptic.co/insights/binance-largest-hack-in-history/"],
      ["CNBC", "https://www.cnbc.com/2026/11/03/binance-co-ceo-teng-says-hackers-used-fake-job-interviews-to-steal-6point3-billion-in-crypto.html"],
      ["CoinDesk中文", "https://www.coindesk.com/zh/business/2026/11/03/binance-s-usd6-3-billion-hack-began-with-a-fake-job-interview-exchange-says"],
      ["慢雾档案", "https://hacked.slowmist.io/zh/?c=Exchange"],
    ],
    "fetchSources": [
      {"id": "elliptic", "label": "Elliptic", "url": "https://www.elliptic.co/insights/binance-largest-hack-in-history/"},
      {"id": "cnbc", "label": "CNBC", "url": "https://www.cnbc.com/2026/11/03/binance-co-ceo-teng-says-hackers-used-fake-job-interviews-to-steal-6point3-billion-in-crypto.html"},
      {"id": "slowmist", "label": "慢雾档案", "url": "https://hacked.slowmist.io/zh/?c=Exchange"},
    ],
    "watchPhrases": ["frozen", "SAFU", "withdrawal", "TraderTraitor", "EIP-7702", "interview", "replenish", "冻结", "提币", "补足", "朝鲜", "面试"],
  },
  "mercado_20261102": {
    "id": "mercado_20261102",
    "name": "Mercado Bitcoin · 2026-11-02 多链钱包被盗",
    "exchange": "Mercado Bitcoin",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 48600000,
    "lossLabel": "约 $40–48.6 百万",
    "summary": "巴西交易所多链钱包/客户充值地址被抽干。官方称已遏制、客户不受损并暂停充提。Bitquery显示官方宣称遏制后约4小时以太坊充值地址仍被清空；损失上修至约$4860万；已冻结逾$1500万。疑与同日BitMart同一攻击者。",
    "kpis": [
      {"n": "~$40–48.6M", "l": "跨约10条链"},
      {"n": "充提暂停", "l": "预防性措施"},
      {"n": ">$15M", "l": "已冻结"},
      {"n": "+4小时", "l": "宣称遏制后仍外流"},
      {"n": "全额覆盖承诺", "l": "平台承担"},
      {"n": "疑同团伙", "l": "与BitMart关联"},
    ],
    "statuses": [
      ["事件状态", "调查中", "官方称客户不受损", "warn"],
      ["止血质量", "存疑", "遏制声明后仍失血约4小时", "bad"],
      ["攻击面", "多链签名/充值地址管理", "普通转账非合约漏洞", "bad"],
      ["冻结", ">$15M", "Tether/Circle等", "ok"],
    ],
    "timeline": [
      {"t": "11-02 ~06:19–06:53 UTC", "d": "多链钱包集中外流"},
      {"t": "11-02 12:56 UTC", "d": "官方声明已迅速遏制"},
      {"t": "11-02 12:27–16:56 UTC", "d": "Bitquery：ETH上约36042个充值地址仍被抽"},
      {"t": "11-05", "d": "公开遏制后仍失血与$48.6M上修"},
      {"t": "11-09计划", "d": "官网拟只读开放；充提恢复日期未定"},
    ],
    "fundFlow": [
      ["被盗", "热钱包+大量充值地址", "跨约10链"],
      ["攻击者持仓", "约2852 ETH、106 BTC、10700 SOL等", "早期报告"],
      ["冻结", ">$15M（另有约$11M官方/伙伴口径）", "Tether/Circle/Chainalysis等"],
      ["关联", "同地址收BitMart相关资金", "约$39.1万"],
    ],
    "links": [
      ["CoinDesk初报", "https://www.coindesk.com/business/2026/11/02/brazil-s-mercado-bitcoin-halts-withdrawals-after-usd40-million-drained-across-10-chains"],
      ["遏制后仍失血", "https://www.coindesk.com/business/2026/11/05/mercado-bitcoin-hack-continued-hours-after-exchange-said-attack-was-contained-report-finds"],
      ["慢雾", "https://hacked.slowmist.io/zh/?c=Exchange"],
    ],
    "fetchSources": [
      {"id": "cd1", "label": "CoinDesk初报", "url": "https://www.coindesk.com/business/2026/11/02/brazil-s-mercado-bitcoin-halts-withdrawals-after-usd40-million-drained-across-10-chains"},
      {"id": "cd2", "label": "遏制后仍失血", "url": "https://www.coindesk.com/business/2026/11/05/mercado-bitcoin-hack-continued-hours-after-exchange-said-attack-was-contained-report-finds"},
    ],
    "watchPhrases": ["contained", "withdrawal", "frozen", "Bitquery", "BitMart", "deposit", "暂停", "冻结", "遏制"],
  },
  "bitmart_20261102": {
    "id": "bitmart_20261102",
    "name": "BitMart · 2026-11-02 关联多链热钱包被盗",
    "exchange": "BitMart",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 391000,
    "lossLabel": "约 $39.1 万",
    "summary": "创始人确认11/2被黑。Bitquery将约$39.1万主要关联Base/Arbitrum/Optimism钱包，并指向与Mercado Bitcoin同一攻击者。慢雾称当时处重组清算、安全人力不足。",
    "kpis": [
      {"n": "~$39.1万", "l": "关联损失"},
      {"n": "11/2", "l": "与Mercado同日"},
      {"n": "疑同团伙", "l": "创始人初步口径"},
      {"n": "L2热钱包", "l": "Base/Arb/OP"},
      {"n": "重组期", "l": "安全人力不足"},
      {"n": "小规模", "l": "相对Mercado"},
    ],
    "statuses": [
      ["事件状态", "已确认", "赔付细节少", "warn"],
      ["与Mercado", "高度疑似同一攻击者", "链上地址重叠", "info"],
      ["损失", "约数十万美元", "远小于Mercado", "info"],
      ["运营背景", "重组清算", "安全资源受限", "bad"],
    ],
    "timeline": [
      {"t": "11-02前", "d": "攻击者地址已收疑似BitMart相关L2资金"},
      {"t": "11-02", "d": "创始人确认被黑"},
      {"t": "11-05", "d": "公开约$39.1万关联估算"},
    ],
    "fundFlow": [
      ["被盗", "L2热钱包", "Base/Arb/OP"],
      ["归集", "与Mercado攻击者同体系", "串联基础设施"],
      ["冻结/追回", "公开细节少", "可能随Mercado协作"],
    ],
    "links": [
      ["CoinDesk关联", "https://www.coindesk.com/business/2026/11/05/mercado-bitcoin-hack-continued-hours-after-exchange-said-attack-was-contained-report-finds"],
      ["慢雾", "https://hacked.slowmist.io/zh/?c=Exchange"],
    ],
    "fetchSources": [
      {"id": "cd", "label": "CoinDesk关联", "url": "https://www.coindesk.com/business/2026/11/05/mercado-bitcoin-hack-continued-hours-after-exchange-said-attack-was-contained-report-finds"},
      {"id": "sm", "label": "慢雾", "url": "https://hacked.slowmist.io/zh/?c=Exchange"},
    ],
    "watchPhrases": ["BitMart", "Mercado", "391", "Base", "Arbitrum", "Optimism"],
  },
  "coindcx_202610": {
    "id": "coindcx_202610",
    "name": "CoinDCX · 2026-10-21 退役钱包 15.99M USDT",
    "exchange": "CoinDCX",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 15990000,
    "lossLabel": "15.99M USDT（公司自担）",
    "summary": "10/21 起约 15.99M USDT 从 TRON 上已退役/被标旧的运营钱包外流。官方称该基础设施在 2025-07 事件后已弃用，但自动归集服务一度失效导致用户误充积压；CEO 曾称“假警报”，后博客确认公司吸收损失。Tether 于 10/22 冻结关联约 2.21M USDT（9 地址）。活跃交易/充提口径称未中断。",
    "kpis": [
      {"n": "15.99M USDT", "l": "确认损失"},
      {"n": "~2.21M USDT", "l": "Tether冻结（9地址）"},
      {"n": "先否后认", "l": "CEO曾称假警报"},
      {"n": "退役钱包", "l": "2025-07遗留"},
      {"n": "扫链失败", "l": "自动归集失效"},
      {"n": "公司自担", "l": "用户余额口径安全"},
    ],
    "statuses": [
      ["事件状态", "已确认、公司自担", "活跃系统称未停", "warn"],
      ["沟通", "先否后认", "损害信任", "bad"],
      ["攻击面", "退役钱包+归集失效", "误充积压被抽", "bad"],
      ["冻结", "~2.21M / 15.99M", "大部分已分散", "warn"],
      ["用户", "公司吸收损失口径", "官方博客", "ok"],
    ],
    "timeline": [
      {"t": "10-21", "d": "约15.99M USDT自退役/旧运营地址外流并拆分"},
      {"t": "10-21/22", "d": "CEO一度称假警报；后承认运营损失"},
      {"t": "10-22 22:45 UTC", "d": "Tether冻结9地址约2,212,850 USDT"},
      {"t": "约10-25/26", "d": "官方博客确认15.99M USDT公司吸收"},
    ],
    "fundFlow": [
      ["被盗", "TRON退役运营钱包积压USDT", "含大额单笔约15.82M"],
      ["拆分", "→多个地址/交易所充值", "冻结前大部分已走"],
      ["冻结", "~2.21M USDT", "Tether黑名单9地址"],
      ["赔付", "公司吸收", "活跃冷钱包称隔离"],
    ],
    "links": [
      ["CoinDCX官方更新", "https://coindcx.com/blog/coindcx-news/on-chain-wallet-activity-update-21-oct-2026"],
      ["The Block确认报道", "https://www.theblock.co/news/business/2026-10-25-coindcx-confirms-16-million-loss-from-retired-wallets-days-after-ceo-called-breach-reports-a-false-alarm-431617"],
      ["慢雾", "https://hacked.slowmist.io/zh/?c=Exchange"],
    ],
    "fetchSources": [
      {"id": "official", "label": "CoinDCX官方", "url": "https://coindcx.com/blog/coindcx-news/on-chain-wallet-activity-update-21-oct-2026"},
      {"id": "block", "label": "The Block", "url": "https://www.theblock.co/news/business/2026-10-25-coindcx-confirms-16-million-loss-from-retired-wallets-days-after-ceo-called-breach-reports-a-false-alarm-431617"},
    ],
    "watchPhrases": ["CoinDCX", "USDT", "Tether", "frozen", "deprecated", "15.99", "false alarm", "退役", "冻结", "归集"],
  },
  "bitget_20260924": {
    "id": "bitget_20260924",
    "name": "Bitget · 2026-09-24 热/暖钱包事件",
    "exchange": "Bitget",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 388000000,
    "lossLabel": "约 $3.88 亿",
    "summary": "第三方安全产品0day→高权限→伪造提现。私钥/冷钱包未失陷；保护基金覆盖后补至>$3亿；10/2全量复提。公开冻结约$110万；CEO不指望大量追回。后续分析将部分资金流与AFX/TraderTraitor交叉。",
    "kpis": [
      {"n": "$3.88亿", "l": "核实损失"},
      {"n": "已全量复提", "l": "10/2完成"},
      {"n": "~$110万", "l": "公开冻结"},
      {"n": ">$3亿", "l": "保护基金已补"},
      {"n": "Mandiant/慢雾", "l": "9/30报告"},
      {"n": "疑关联AFX", "l": "链上交叉分析"},
    ],
    "statuses": [
      ["事件状态", "已遏制、运营恢复", "追赃低预期", "ok"],
      ["提币", "已全部恢复", "10/2完成", "ok"],
      ["根因", "第三方安全产品0day", "厂商名未公开", "warn"],
      ["追赃", "进行中、预期有限", "THORChain拒屏蔽", "bad"],
      ["归因", "倾向朝鲜相关", "与AFX有交叉讨论", "info"],
    ],
    "timeline": [
      {"t": "08-31", "d": "慢雾：最早恶意活动"},
      {"t": "09-24", "d": "热/暖未授权转出；约3小时止血"},
      {"t": "09-28→10-02", "d": "分阶段复提完成"},
      {"t": "09-30", "d": "Mandiant+慢雾报告；保护基金>$3亿"},
      {"t": "10-02", "d": "CEO：冻结约$110万；不指望大量追回"},
      {"t": "10月后", "d": "与AFX/TraderTraitor关联讨论增多"},
    ],
    "fundFlow": [
      ["停留", "ETH/XRP/ZEC大头曾长期可见", "持续兑BTC"],
      ["途经", "THORChain/Chainflip/DEX/桥", "主出途BTC"],
      ["冻结", "~$110万", "<0.3%"],
      ["关联", "与AFX气费资助对手方交叉", "分析口径"],
    ],
    "links": [
      ["官方事件页", "https://www.bitget.com/campaigns/bitget-security-incident-2026"],
      ["追踪面板", "https://trace.bgblockchain.xyz/v2#explorer"],
      ["Merkle追踪", "https://www.merklescience.com/blog/hack-track-bitget-drained-of-388m--tracing-where-the-funds-went"],
    ],
    "fetchSources": [
      {"id": "official", "label": "Bitget官方", "url": "https://www.bitget.com/campaigns/bitget-security-incident-2026"},
      {"id": "holdings", "label": "Holdings API", "url": "https://trace.bgblockchain.xyz/api/holdings", "raw": True},
    ],
    "watchPhrases": ["frozen", "Protection Fund", "withdrawal", "Mandiant", "SlowMist", "提币", "冻结", "追回"],
  },
  "afx_20260722": {
    "id": "afx_20260722",
    "name": "AFX · 2026-07-22 托管桥被盗",
    "exchange": "AFX",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 24150000,
    "lossLabel": "约 $2415 万 USDC",
    "summary": "自营托管桥热验证者密钥失陷达法定人数，约2415万USDC被转出并兑ETH。非Arb原生桥。官方倾向UNC4899/TraderTraitor；goodwill细节弱。与Phemex关联及后续Bitget资金流交叉讨论持续。",
    "kpis": [
      {"n": "$2415万", "l": "USDC"},
      {"n": "桥签名失陷", "l": "热验证者法定人数"},
      {"n": "非Arb原生桥", "l": "已澄清"},
      {"n": "DPRK倾向", "l": "官方/情报口径"},
      {"n": "goodwill", "l": "补偿细节仍弱"},
      {"n": "疑串Bitget", "l": "后续分析"},
    ],
    "statuses": [
      ["事件状态", "技术复盘已出", "补偿闭环不足", "warn"],
      ["攻击面", "桥验证者密钥", "链上逻辑按设计执行", "bad"],
      ["归因", "TraderTraitor倾向", "非司法终局", "info"],
      ["关联", "Phemex/Bitget叙事", "需证据分层", "warn"],
    ],
    "timeline": [
      {"t": "07-22", "d": "托管桥被盗约2415万USDC"},
      {"t": "07月下旬", "d": "Post-mortem；澄清非Arb原生桥"},
      {"t": "08-03前后", "d": "曾预告goodwill"},
      {"t": "09月后", "d": "与Bitget资金流交叉分析出现"},
    ],
    "fundFlow": [
      ["被盗", "桥内USDC", "验证者共签"],
      ["转移", "→ETH", "快速变现"],
      ["补偿", "goodwill/赏金", "公开落地有限"],
    ],
    "links": [
      ["Post-Mortem", "https://medium.com/@AFXTrade/a-detailed-post-mortem-on-the-afx-security-incident-57d564ef812f"],
      ["CoinDesk", "https://www.coindesk.com/tech/2026/07/23/arbitrum-based-afx-trade-drained-of-usd24-million-after-bridge-keys-compromised"],
    ],
    "fetchSources": [
      {"id": "pm", "label": "AFX Post-Mortem", "url": "https://medium.com/@AFXTrade/a-detailed-post-mortem-on-the-afx-security-incident-57d564ef812f"},
    ],
    "watchPhrases": ["goodwill", "USDC", "bridge", "TraderTraitor", "validator", "补偿", "桥"],
  },
  "triplea_20260725": {
    "id": "triplea_20260725",
    "name": "Triple-A · 2026-07 公司金库事件",
    "exchange": "Triple-A",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 11800000,
    "lossLabel": "约 $1180 万（公司金库）",
    "summary": "新加坡支付公司金库未授权访问；客户信托资金未损。数小时遏制恢复。社工+提权；警方/MAS协作。后续有混币路径报道。",
    "kpis": [
      {"n": "~$1180万", "l": "公司金库"},
      {"n": "客户未损", "l": "信托隔离"},
      {"n": "数小时遏制", "l": "服务已恢复"},
      {"n": "社工入口", "l": "非产品漏洞口径"},
      {"n": "多链金库", "l": "权限集中风险"},
      {"n": "追赃谨慎", "l": "不夸大返还"},
    ],
    "statuses": [
      ["事件状态", "已遏制", "业务正常", "ok"],
      ["客户资金", "未受影响", "信托账户", "ok"],
      ["攻击", "社工+提权", "金库权限集中", "warn"],
      ["追赃", "进行中", "混币增加难度", "bad"],
    ],
    "timeline": [
      {"t": "2026-07-24/25", "d": "金库未授权访问；短暂维护后恢复"},
      {"t": "事后", "d": "Post-mortem：客户未损"},
      {"t": "后续", "d": "链上混币等转移报道"},
    ],
    "fundFlow": [
      ["被盗", "公司金库钱包", "跨多链"],
      ["客户", "信托隔离", "未暴露"],
      ["洗钱", "含混币路径", "追回困难"],
    ],
    "links": [
      ["Post-Mortem", "https://www.triple-a.io/blog/blog-incident-post-mortem"],
    ],
    "fetchSources": [
      {"id": "pm", "label": "Triple-A Post-Mortem", "url": "https://www.triple-a.io/blog/blog-incident-post-mortem"},
    ],
    "watchPhrases": ["client funds", "treasury", "recovery", "客户", "金库", "追回"],
  },
  "phemex_202501": {
    "id": "phemex_202501",
    "name": "Phemex · 2025-01 热钱包事件",
    "exchange": "Phemex",
    "baselineUpdated": "2026-11-07",
    "lossUsd": 85000000,
    "lossLabel": "约 $0.7–0.85 亿",
    "summary": "2025-01热钱包被盗，官方称储备全额赔付。PoR仍报超储但绝对储备曾收缩。与AFX存在公开关联叙事。",
    "kpis": [
      {"n": "~$0.7–0.85亿", "l": "热钱包被盗"},
      {"n": "全额赔付口径", "l": "公司储备"},
      {"n": "PoR超储", "l": "比率仍可>100%"},
      {"n": "AFX关联", "l": "体系线索"},
      {"n": "持续运营", "l": "主站未关停"},
      {"n": "长期观测", "l": "储备与出金"},
    ],
    "statuses": [
      ["事件状态", "历史+持续观测", "主站运营中", "info"],
      ["赔付", "官方全额覆盖", "追赃公开有限", "ok"],
      ["PoR", "比率超储", "对照绝对储备", "warn"],
      ["AFX", "强关联叙事", "表外风险", "bad"],
    ],
    "timeline": [
      {"t": "2025-01", "d": "热钱包事件；储备赔付"},
      {"t": "2026-07", "d": "关联AFX桥被盗"},
      {"t": "2026-08+", "d": "PoR与绝对储备交叉验证"},
    ],
    "fundFlow": [
      ["被盗", "热钱包", "公司储备赔付"],
      ["用户", "官方称不受损", "依赖偿付可信度"],
      ["关联", "AFX表外", "PoR未必覆盖"],
    ],
    "links": [
      ["Phemex", "https://phemex.com"],
      ["DefiLlama", "https://defillama.com/cexs"],
    ],
    "fetchSources": [
      {"id": "home", "label": "Phemex", "url": "https://phemex.com"},
      {"id": "llama", "label": "DefiLlama", "url": "https://defillama.com/cexs"},
    ],
    "watchPhrases": ["Proof of Reserves", "PoR", "Phemex", "AFX", "储备", "security"],
  },
}

HEAD = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>交易所被盗案件进展追踪</title>
<style>
  :root {
    --bg: #f4f1ea; --card: #fffdf8; --ink: #1a1f24; --muted: #5c6570; --line: #e4ddd2;
    --teal: #0d585c; --teal-soft: #e7f3f2; --amber: #9a6b12; --amber-soft: #fff6e5;
    --red: #a0332c; --red-soft: #ffefed; --blue: #1f4f86; --blue-soft: #eaf1f8; --header: #142f38;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: "PingFang SC","Noto Sans CJK SC","WenQuanYi Micro Hei","Microsoft YaHei",sans-serif;
    color: var(--ink); line-height: 1.65;
    background: radial-gradient(900px 420px at 0% 0%, #e5efe8 0%, transparent 55%),
      radial-gradient(800px 380px at 100% 0%, #f0e6d8 0%, transparent 50%), var(--bg);
  }
  .wrap { max-width: 980px; margin: 0 auto; padding: 24px 16px 64px; }
  header {
    background: linear-gradient(140deg, #142f38 0%, #1d4a52 60%, #275846 100%);
    color: #f7f4ee; border-radius: 22px; padding: 24px 22px; margin-bottom: 18px;
  }
  header h1 { margin: 0 0 8px; font-size: 1.55rem; }
  header p { margin: 0; opacity: .9; font-size: .92rem; }
  .toolbar { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 16px; }
  select, button { font: inherit; border-radius: 12px; border: 1px solid rgba(255,255,255,.25); padding: 10px 14px; }
  select { background: rgba(255,255,255,.12); color: #fff; max-width: 100%; }
  select option { color: #111; }
  button.primary { background: #f3efe6; color: var(--header); border: none; font-weight: 700; cursor: pointer; }
  button.primary:disabled { opacity: .6; cursor: wait; }
  button.ghost { background: transparent; color: #fff; cursor: pointer; }
  .status-line { font-size: .85rem; opacity: .85; margin-top: 10px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 14px 0 18px; }
  .kpi { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px; }
  .kpi .n { font-size: 1.15rem; font-weight: 750; color: var(--teal); }
  .kpi .l { font-size: .78rem; color: var(--muted); margin-top: 3px; }
  .card { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; margin-bottom: 14px; }
  .card h2 { margin: 0 0 12px; font-size: 1.05rem; border-left: 4px solid var(--teal); padding-left: 10px; }
  .delta { border: 1px solid #e3d2a8; background: var(--amber-soft); border-radius: 16px; padding: 14px 16px; margin-bottom: 14px; display: none; }
  .delta.show { display: block; }
  .delta h2 { margin: 0 0 8px; font-size: 1.05rem; color: var(--amber); }
  .delta ul { margin: 8px 0 0; padding-left: 18px; }
  .tag { display: inline-block; font-size: .72rem; padding: 2px 8px; border-radius: 999px; margin-right: 6px; }
  .tag.ok { background: var(--teal-soft); color: var(--teal); }
  .tag.warn { background: var(--amber-soft); color: var(--amber); }
  .tag.bad { background: var(--red-soft); color: var(--red); }
  .tag.info { background: var(--blue-soft); color: var(--blue); }
  table { width: 100%; border-collapse: collapse; font-size: .9rem; }
  th, td { text-align: left; padding: 8px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { color: var(--muted); font-weight: 600; font-size: .8rem; }
  .timeline { list-style: none; padding: 0; margin: 0; }
  .timeline li { position: relative; padding: 0 0 14px 18px; border-left: 2px solid var(--line); margin-left: 6px; }
  .timeline li:last-child { padding-bottom: 0; }
  .timeline li::before { content: ""; width: 10px; height: 10px; border-radius: 50%; background: var(--teal); position: absolute; left: -6px; top: 5px; }
  .timeline .t { font-weight: 700; font-size: .9rem; }
  .timeline .d { color: var(--muted); font-size: .86rem; }
  .links a { color: var(--teal); word-break: break-all; }
  .muted { color: var(--muted); font-size: .85rem; }
  .err { background: var(--red-soft); color: var(--red); border-radius: 10px; padding: 8px 10px; font-size: .85rem; margin-top: 8px; display: none; }
  .err.show { display: block; }
  pre.fetch { white-space: pre-wrap; background: #f6f2ea; border-radius: 10px; padding: 10px; font-size: .78rem; max-height: 220px; overflow: auto; display: none; }
  pre.fetch.show { display: block; }
  footer { margin-top: 18px; color: var(--muted); font-size: .8rem; }
  .banner { background: #fff8ec; border: 1px solid #e3d2a8; border-radius: 12px; padding: 10px 14px; margin-bottom: 14px; font-size: .9rem; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>交易所被盗案件进展追踪</h1>
    <p>已收录 Binance / Mercado Bitcoin / BitMart / CoinDCX / Bitget / Phemex / Triple-A / AFX。点「更新」拉公开源并对比上次快照。</p>
    <div class="toolbar">
      <select id="caseSelect" aria-label="选择案件"></select>
      <button class="primary" id="btnUpdate">更新</button>
      <button class="ghost" id="btnReset">重置本地快照</button>
      <button class="ghost" id="btnExport">导出 JSON</button>
    </div>
    <div class="status-line" id="statusLine">尚未更新 · 当前显示内置基线</div>
    <div class="err" id="errBox"></div>
  </header>

  <div class="banner">基线日期：<strong>2026-11-07</strong> · 默认显示最新大案 Binance。切换下拉可看其他案件。</div>
  <div class="delta" id="deltaBox"><h2>相对上次的最新变化</h2><div id="deltaBody"></div></div>
  <div class="grid" id="kpiGrid"></div>
  <section class="card"><h2>案件摘要</h2><div id="summary"></div></section>
  <section class="card"><h2>关键节点</h2>
    <table><thead><tr><th>维度</th><th>状态</th><th>备注</th></tr></thead><tbody id="statusTable"></tbody></table>
  </section>
  <section class="card"><h2>时间线</h2><ul class="timeline" id="timeline"></ul></section>
  <section class="card"><h2>资金停留 / 在途 / 出途</h2><div id="fundFlow"></div></section>
  <section class="card"><h2>官方与追踪链接</h2><div class="links" id="links"></div></section>
  <section class="card"><h2>本次更新抓取原文</h2>
    <p class="muted">点击更新后显示公开源文本片段。</p>
    <pre class="fetch" id="fetchDump"></pre>
  </section>
  <footer>仅供信息追踪，非投资建议。数据保存在浏览器 localStorage。</footer>
</div>
<script>
'''

TAIL = r'''
const STORAGE_KEY = "cex_hack_tracker_v2";
function $(id){return document.getElementById(id);}
function loadStore(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||"{}");}catch(e){return {};}}
function saveStore(s){localStorage.setItem(STORAGE_KEY, JSON.stringify(s));}
function currentCaseId(){return $("caseSelect").value || "binance_20261029";}
function tagLabel(t){return ({ok:"闭环/正常",warn:"关注",bad:"风险/未闭环",info:"信息"})[t]||t;}
function escapeHtml(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}

function renderCase(caseId){
  const c=CASES[caseId]; if(!c) return;
  $("kpiGrid").innerHTML=c.kpis.map(k=>`<div class="kpi"><div class="n">${k.n}</div><div class="l">${k.l}</div></div>`).join("");
  $("summary").innerHTML=`<p>${c.summary}</p><p class="muted">内置基线：${c.baselineUpdated} · ${c.exchange} · ${c.lossLabel}</p>`;
  $("statusTable").innerHTML=c.statuses.map(([a,b,note,tag])=>`<tr><td>${a}</td><td><span class="tag ${tag}">${tagLabel(tag)}</span>${b}</td><td class="muted">${note}</td></tr>`).join("");
  $("timeline").innerHTML=c.timeline.map(x=>`<li><div class="t">${x.t}</div><div class="d">${x.d}</div></li>`).join("");
  $("fundFlow").innerHTML=`<table><thead><tr><th>状态</th><th>内容</th><th>备注</th></tr></thead><tbody>`+
    c.fundFlow.map(r=>`<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td class="muted">${r[2]}</td></tr>`).join("")+`</tbody></table>`;
  $("links").innerHTML=c.links.map(([n,u])=>`<div style="margin:6px 0"><a href="${u}" target="_blank" rel="noopener">${n}</a></div>`).join("");
  const snap=loadStore()[caseId];
  if(snap&&snap.lastCheckAt){
    $("statusLine").textContent=`上次更新：${snap.lastCheckAt} · 内置基线：${c.baselineUpdated}`;
    if(snap.lastDeltaHtml){$("deltaBox").classList.add("show");$("deltaBody").innerHTML=snap.lastDeltaHtml;}
  }else{
    $("statusLine").textContent=`尚未在本机点过更新 · 显示内置基线（${c.baselineUpdated}）`;
  }
}

async function fetchViaProxy(url, raw){
  const targets = raw ? [url, `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`]
    : [`https://r.jina.ai/${url}`, `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`];
  let lastErr;
  for(const t of targets){
    try{
      const ctrl=new AbortController();
      const timer=setTimeout(()=>ctrl.abort(),20000);
      const res=await fetch(t,{signal:ctrl.signal});
      clearTimeout(timer);
      if(!res.ok) throw new Error("HTTP "+res.status);
      const text=await res.text();
      if(!text||text.length<20) throw new Error("空响应");
      return {ok:true, via:t, text};
    }catch(e){lastErr=e;}
  }
  return {ok:false, error:String(lastErr&&lastErr.message||lastErr)};
}

function summarizeHoldings(text){
  try{
    const data=JSON.parse(text);
    const arr=Array.isArray(data)?data:Array.isArray(data.data)?data.data:Array.isArray(data.addresses)?data.addresses:Array.isArray(data.items)?data.items:null;
    if(!arr) return {fingerprint:text.slice(0,500), note:"Holdings 非数组"};
    return {fingerprint:`addresses=${arr.length}`, note:`API 地址数 ${arr.length}`};
  }catch(e){return {fingerprint:text.slice(0,500), note:"Holdings 解析失败"};}
}

function extractHits(text, phrases){
  const lower=text.toLowerCase();
  const hits=phrases.filter(p=>lower.includes(p.toLowerCase()));
  const lines=text.split(/\n+/).map(s=>s.trim()).filter(Boolean);
  const interesting=lines.filter(l=>/2026|October|November|withdrawal|frozen|hack|Mandiant|SlowMist|提币|冻结|追回|被盗|黑客/i.test(l)).slice(0,12);
  return {hits, interesting};
}

async function doUpdate(){
  const caseId=currentCaseId(); const c=CASES[caseId];
  const btn=$("btnUpdate"); const err=$("errBox");
  err.classList.remove("show"); btn.disabled=true; btn.textContent="更新中…";
  $("statusLine").textContent="正在拉取公开源…";
  const store=loadStore(); const prev=store[caseId]||{};
  const stamp=new Date().toISOString().replace("T"," ").slice(0,19)+" UTC";
  const dumps=[], fingerprints={}, notes=[], interestingAll=[];
  for(const src of (c.fetchSources||[])){
    const r=await fetchViaProxy(src.url, !!src.raw);
    if(!r.ok){notes.push("❌ "+src.label+"：失败（"+r.error+"）"); continue;}
    notes.push("✅ "+src.label+"：成功（"+r.text.length+" 字符）");
    dumps.push("===== "+src.label+" =====\n"+r.text.slice(0,6000));
    if(src.id==="holdings"){
      const h=summarizeHoldings(r.text); fingerprints.holdings=h.fingerprint; interestingAll.push("[Holdings] "+h.note);
    }else{
      const extracted=extractHits(r.text, c.watchPhrases||[]);
      fingerprints[src.id]=extracted.hits.sort().join("|")+"::"+extracted.interesting.slice(0,5).join("||");
      extracted.interesting.forEach(x=>interestingAll.push("["+src.label+"] "+x.slice(0,180)));
    }
  }
  const prevFp=prev.fingerprints||{};
  const changed=Object.keys(fingerprints).filter(k=>prevFp[k]!==fingerprints[k]);
  let deltaHtml="";
  if(!prev.lastCheckAt){
    deltaHtml=`<p>本机<strong>第一次</strong>更新（${stamp}）。下次将只显示变化。</p>`;
    if(interestingAll.length) deltaHtml+="<ul>"+interestingAll.slice(0,8).map(x=>"<li>"+escapeHtml(x)+"</li>").join("")+"</ul>";
  }else if(!changed.length){
    const anyOk=notes.some(n=>n.startsWith("✅"));
    deltaHtml = !anyOk
      ? `<p>本次源拉取失败。</p><ul>`+notes.map(n=>"<li>"+escapeHtml(n)+"</li>").join("")+"</ul>"
      : `<p>相对上次（${prev.lastCheckAt}）：指纹<strong>无明显变化</strong>。</p>`;
  }else{
    deltaHtml=`<p>相对上次（${prev.lastCheckAt}）变化源：<strong>${changed.join(", ")}</strong></p>`;
    const uniq=[...new Set(interestingAll)].slice(0,10);
    if(uniq.length) deltaHtml+="<ul>"+uniq.map(x=>"<li>"+escapeHtml(x)+"</li>").join("")+"</ul>";
  }
  deltaHtml+=`<p class="muted" style="margin-top:10px">${notes.map(escapeHtml).join("<br>")}</p>`;
  store[caseId]={lastCheckAt:stamp, fingerprints, lastDeltaHtml:deltaHtml, lastDump:dumps.join("\n\n").slice(0,50000)};
  saveStore(store);
  $("deltaBox").classList.add("show"); $("deltaBody").innerHTML=deltaHtml;
  $("statusLine").textContent=`上次更新：${stamp} · 内置基线：${c.baselineUpdated}`;
  if(dumps.length){$("fetchDump").textContent=dumps.join("\n\n"); $("fetchDump").classList.add("show");}
  if(!dumps.length){err.textContent="全部源拉取失败。可稍后重试或让助手刷新基线。"; err.classList.add("show");}
  btn.disabled=false; btn.textContent="更新";
}

function init(){
  const sel=$("caseSelect");
  const order=["binance_20261029","mercado_20261102","bitmart_20261102","coindcx_202610","bitget_20260924","afx_20260722","triplea_20260725","phemex_202501"];
  sel.innerHTML=order.filter(id=>CASES[id]).map(id=>`<option value="${id}">${CASES[id].name}</option>`).join("");
  sel.addEventListener("change",()=>{$("deltaBox").classList.remove("show");$("fetchDump").classList.remove("show");renderCase(sel.value);});
  $("btnUpdate").addEventListener("click", doUpdate);
  $("btnReset").addEventListener("click",()=>{const s=loadStore();delete s[currentCaseId()];saveStore(s);$("deltaBox").classList.remove("show");$("fetchDump").classList.remove("show");renderCase(currentCaseId());$("statusLine").textContent="已清除本机快照";});
  $("btnExport").addEventListener("click",()=>{
    const payload={exportedAt:new Date().toISOString(), caseId:currentCaseId(), baseline:CASES[currentCaseId()], localSnapshot:loadStore()[currentCaseId()]||null};
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});
    const a=document.createElement("a"); a.href=URL.createObjectURL(blob); a.download=currentCaseId()+"-tracker-export.json"; a.click(); URL.revokeObjectURL(a.href);
  });
  renderCase(currentCaseId());
}
init();
</script>
</body>
</html>
'''


def main():
    cases_json = json.dumps(CASES, ensure_ascii=False, indent=2)
    full = HEAD + "\nconst CASES = " + cases_json + ";\n" + TAIL
    Path("/workspace/cex-hack-tracker").mkdir(parents=True, exist_ok=True)
    Path("/opt/cursor/artifacts").mkdir(parents=True, exist_ok=True)
    outs = [
        Path("/workspace/cex-hack-tracker.html"),
        Path("/workspace/cex-hack-tracker/index.html"),
        Path("/opt/cursor/artifacts/cex-hack-tracker.html"),
    ]
    for p in outs:
        p.write_text(full, encoding="utf-8")
        print(f"wrote {p} ({p.stat().st_size} bytes)")
    print("cases:", len(CASES))


if __name__ == "__main__":
    main()

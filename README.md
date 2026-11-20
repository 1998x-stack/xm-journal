# xm-journal

**把每天的进展，沉淀为长期的认知资产。** 一个面向持续研究、工程实践、学习与项目管理的个人日志系统。以每日记录为事实源，自动形成周度复盘和月度可视化汇报。

[![Pages](https://github.com/1998x-stack/xm-journal/actions/workflows/pages.yml/badge.svg)](https://github.com/1998x-stack/xm-journal/actions/workflows/pages.yml)

- **网站**：https://1998x-stack.github.io/xm-journal/
- **每日记录**：journal/daily/YYYY/MM/YYYY-MM-DD.md
- **周报**：reports/weekly/YYYY/weekly-YYYY-Www.html
- **月报**：reports/monthly/YYYY/monthly-YYYY-MM.html

> 记录原则：事实先于观点，证据先于结论，复盘服务于下一步行动。未知值标记为“未记录”，绝不伪造为 0。

## 1. 项目目标

xm-journal 不是简单的 Markdown 日记集合，而是一套可持续运行的个人知识运营系统：

1. 每天把与 ChatGPT 的讨论、分析、任务进展、决策和结果沉淀为结构化日志。
2. 每天生成一份可视化日报，保留上下文、完成事项、证据、风险和下一步。
3. 每周日完成当天记录后，额外生成覆盖周一至周日的周报。
4. 每月最后一天完成当天记录后，额外生成覆盖整月的月报。
5. 在周末与月末重合时，同时生成日报、周报、月报，不能互相覆盖或遗漏。
6. 对历史记录补充或修订时，自动识别受影响的周报/月报并重新生成。

## 2. 报告周期与触发规则

| 报告 | 时间范围 | 生成时机 | 核心问题 |
|---|---|---|---|
| 日报 | 单个自然日 | 当天记录整理完成后 | 今天发生了什么？证据是什么？ |
| 周报 | ISO 周：周一至周日 | 周日当天记录完成后 | 本周取得了什么进展？哪些问题反复出现？ |
| 月报 | 自然月 1 日至月末 | 月末当天记录完成后 | 本月的阶段成果、趋势和方向是什么？ |

时区默认 **Asia/Shanghai**。周使用 ISO-8601 规则，跨年时按 ISO week-year 命名，例如 2027 年 1 月 1 日属于 2026-W53。

**边界日多报告规则：**
- 普通工作日：日报。
- 周日但非月末：日报 + 周报。
- 月末但非周日：日报 + 月报。
- 同时为周日和月末：日报 + 周报 + 月报。

报告只有在周期内所有预期日期均被检查后才能标记为“最终版”。未记录的日期必须显示为数据缺口，不能补写虚构活动。可以生成中期预览，但必须明确标注“暂定”。

## 3. 分类体系

每条日报记录只指定一个主分类，跨领域信息使用标签关联。

| 分类 | slug | 范围 |
|---|---|---|
| 研究与论文 | research | 论文阅读、研究问题、实验、技术调研 |
| 工程与技术 | engineering | 编码、架构、调试、性能、CI/CD、部署 |
| 学习与成长 | learning | 知识学习、课程、练习、技能积累 |
| 产品与设计 | product | 产品方向、需求、体验、交付 |
| 运营与流程 | operations | 计划、流程、指标、自动化 |
| 协作与沟通 | collaboration | 会议、评审、反馈、依赖 |
| 复盘与思考 | reflection | 经验、原则、反思、改进 |

标签使用小写 kebab-case，优先复用 data/taxonomy.json 中的既有标签，例如 llm、agents、evaluation、ci-cd、github-actions、visualization、planning、automation、performance、debugging、decision、risk。不要为同义词创建重复标签。

详细规则见 [docs/taxonomy.md](docs/taxonomy.md)。

## 4. 每日记录标准

建议每条日报包含：

- 今日概览：当天最重要的 1–3 件事。
- 工作流：按项目或主题组织，而不是堆砌聊天记录。
- 完成事项：明确交付物、链接、PR、commit、部署或可验证结果。
- 研究与学习：问题、理解、证据、仍不确定的地方。
- 关键决策：选择、原因、备选方案及影响。
- 阻塞与风险：现状、影响、依赖和解除条件。
- 指标：数值、单位、统计口径、时间范围与来源。
- 下一步：优先级明确、可执行的动作。
- 来源：对话、GitHub、文档或用户提供的材料。

推荐目录：`journal/daily/YYYY/MM/YYYY-MM-DD.md`。日报是事实源，周报和月报引用日报，不重复维护第二份事实。

## 5. 周报 / 月报的可视化内容

周报和月报不只是把日报拼接起来，而是形成有证据的分析：

1. 结论摘要：3–5 条重要发现。
2. KPI 概览：完成事项、活跃工作流、决策、阻塞、记录覆盖天数。
3. 时间线：重要里程碑、交付与转折。
4. 工作流分析：目标、进展、证据、影响、当前状态。
5. 分类分布：研究、工程、学习等主题变化。
6. 决策记录：关键选择与原因。
7. 风险与阻塞：反复出现的问题、依赖与待解决事项。
8. 经验教训：哪些做法有效，哪些需要改变。
9. 下周期计划：优先级、依赖和可验证完成条件。

图表必须有明确的分析目的。时间范围、单位、样本量、数据缺口都要标明。SVG 应原创、可读、适配手机，并提供文字解释。

## 6. 仓库结构

```text
xm-journal/
├── README.md
├── AGENTS.md
├── journal/
│   └── daily/YYYY/MM/YYYY-MM-DD.md
├── data/
│   ├── taxonomy.json
│   └── entries.json
├── reports/
│   ├── daily/
│   ├── weekly/YYYY/
│   ├── monthly/YYYY/
│   └── index.json
├── skills/
│   ├── journal-reporting/          # 日志系统专属 Skill
│   └── olah-style-journal/         # 从 xm-posts 迁移的原始 Skill 与资源
├── docs/
│   ├── architecture.md
│   ├── taxonomy.md
│   └── reporting-calendar.md
├── site/
│   ├── index.html
│   └── assets/
├── scripts/
│   ├── build_site.py
│   └── validate_site.py
├── tests/
├── requirements-dev.txt
└── .github/workflows/pages.yml
```

## 7. Skills：继承与分工

本仓库保留从 [xm-posts](https://github.com/1998x-stack/xm-posts) 迁移的 Olah-style Skill，包括原始主说明、HTML/CSS 模板、SVG 提取、浏览器检查、数学排版、证据引用、叙事结构和发布参考资料。

但两类 Skill 有明确分工：

- `skills/olah-style-journal/`：迁移来的内容表达、可视化、HTML、SVG、证据与 QA 方法。保留上游来源，不把论文写作步骤机械套用到日志。
- `skills/journal-reporting/SKILL.md`：本项目的主工作流，负责日报采集、分类、周/月聚合、时间边界、证据追溯与报告生成。

今后每次日报整理、周报/月报生成或历史复盘，都应先阅读根目录 [AGENTS.md](AGENTS.md) 和 journal-reporting Skill。

## 8. 本地开发与验证

需要 Python 3.11+：

```bash
git clone https://github.com/1998x-stack/xm-journal.git
cd xm-journal
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/build_site.py
python scripts/validate_site.py
cd _site
python -m http.server 8000
```

打开 http://localhost:8000/。生成目录 `_site/` 不提交到 Git。

## 9. GitHub Pages

工作流在 PR 上运行测试与静态构建；只有 main 分支 push 才部署 Pages。请在仓库 Settings → Pages → Build and deployment 中选择 **GitHub Actions**。实际发布以 Actions 的部署任务成功且网站 URL 可访问为准。PR CI 通过不等于网站已上线。

## 10. 数据质量、隐私与来源

- 不虚构完成事项、指标、日期、工作量、因果关系或成果。
- 计划不等于完成；讨论不等于交付；PR 创建不等于合并；合并不等于部署。
- 指标必须保留单位、分母、统计口径和来源。
- 对历史记录的更正应保留说明，并重新生成相关周期报告。
- 不写入密码、访问令牌、个人身份号码或未经授权的第三方机密。
- 引用 GitHub、论文、文档等来源时保留链接和访问日期。

## 11. 当前阶段

仓库正在建立基础架构。当前已有分类、AGENTS、报告日历、日志专属 Skill、迁移的 Olah-style Skill 资源、静态首页和初始校验脚本。下一阶段将实现结构化日报解析、自动日报/周报/月报生成、可视化图表、完整测试和 Pages 自动部署。

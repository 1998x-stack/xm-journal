# xm-journal

**把每天说出来的，变成看得见的思考。**

xm-journal 是一个以个人口述为入口的可视化日志网站。你只需要自然地讲述今天经历了什么、遇到什么问题、产生了什么想法、有哪些感悟和明天准备做什么；AI 按照仓库中的 **Olah-style-journal Skill** 理解、整理，并将其制作成独立的 SVG 可视化 HTML 文章。

<p align="center">
  <a href="https://1998x-stack.github.io/xm-journal/"><strong>打开每日视觉日志 →</strong></a>
</p>

[![Pages](https://github.com/1998x-stack/xm-journal/actions/workflows/pages.yml/badge.svg)](https://github.com/1998x-stack/xm-journal/actions/workflows/pages.yml)

## 这是什么

它不是项目管理系统，也不是 GitHub 活动仪表盘。

它只做一件事：

**把你每天自然说出来的内容，变成一篇值得回看、容易理解、具有独立视觉表达的个人日志。**

~~~text
每天自然口述
     │
     ▼
理解语境、事实、情绪、问题与计划
     │
     ▼
整理成每日 Markdown 原稿
     │
     ▼
提炼一条主线，设计专属视觉叙事
     │
     ├── 原创 SVG 图解
     ├── 时间线 / 因果图 / 思维模型
     └── 有意义的交互演示
     │
     ▼
独立 HTML 文章
     │
     ▼
首页自动生成卡片 → GitHub Pages
~~~

## 设计原则

### 1. 口述优先，而不是表格优先

不要求你按固定表格讲话，也不要求每次提供项目名称、工时、Commit 或 PR。可以像和朋友聊天一样自然表达。AI 负责整理，不要求你先把想法组织得很完美。

### 2. 保留真实的个人声音

文章区分：

- **事实**：明确发生的事情。
- **感受**：当时的情绪和主观体验。
- **判断**：你对问题的理解。
- **洞察**：从经历中提炼出的规律。
- **计划**：尚未发生、准备执行的事情。
- **待研究问题**：已经意识到但还没有弄懂的内容。

不会把 AI 的推断写成你的亲身经历，也不会把计划写成成果。

### 3. 使用 Olah 风格渐进解释

每篇文章从一个真实场景或问题开始，逐步展开背景、矛盾、变化、理解和行动。图解服务于解释：用原创 SVG 呈现时间线、因果关系、认知闭环、决策过程或习惯机制；需要时加入可操作的交互状态。

### 4. 每篇文章都有自己的视觉表达

不使用一张通用封面覆盖所有文章。每篇文章根据当天内容设计专属的视觉主题、图解和交互；没有必要的图表不为了数量而添加。

## 如何使用

在 ChatGPT 中直接口述，或者把语音转写文本发给 AI。例如：

> 帮我复盘一下今天。我早上起床有点拖延，白天主要在处理工作反馈，晚上又想了很多关于 AI 学习的问题……

随后要求：

> 按照 xm-journal 的 AGENTS.md 和 skills/olah-style-journal/SKILL.md，把这段口述整理成今日原稿，并制作对应的 Olah 风格可视化 HTML，完成检查后发布。

AI 应完成：

1. 阅读本仓库的 AGENTS.md 和 Olah-style-journal Skill。
2. 理解口述内容，保留事实、感受、判断和计划的边界。
3. 更新 journal/daily/YYYY/MM/YYYY-MM-DD.md。
4. 创建 posts/YYYY/MM/YYYY-MM-DD/index.html。
5. 为文章制作独立 SVG、来源记录和必要交互。
6. 构建、校验、运行浏览器 QA，并提交发布。

**说明：** 仓库本身不录音，也不内置语音识别服务。你可以直接使用 ChatGPT 语音对话，或提供语音转写文本；仓库负责保存整理后的内容并生成视觉文章。

## 内容目录

~~~text
xm-journal/
├── AGENTS.md
├── README.md
├── journal/
│   ├── daily/YYYY/MM/YYYY-MM-DD.md       # 每日文字原稿
│   └── templates/daily-template.md
├── posts/
│   └── YYYY/MM/YYYY-MM-DD/
│       ├── index.html                    # 每日视觉文章
│       ├── evidence.json                 # 内容来源与编辑归纳
│       └── assets/                       # 本篇文章专属 SVG
├── skills/
│   └── olah-style-journal/               # 从 Olah-style-posts 迁入并改造
├── site/
│   ├── index.html                        # 文章首页模板
│   └── assets/
├── scripts/
│   ├── build_site.py                     # 文章发现与静态构建
│   ├── validate_site.py                  # 结构与资源校验
│   └── browser_qa.py                     # 全文章浏览器检查
├── tests/
├── docs/
│   ├── architecture.md
│   └── taxonomy.md
└── .github/workflows/pages.yml
~~~

## Olah-style-journal Skill

本仓库内置的 Skill 源自 [1998x-stack/Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts)，保留其渐进叙事、语义 HTML、原创 SVG、响应式排版、轻量交互和浏览器 QA 资产，并将论文讲解流程改造成适合个人口述复盘的内容生产流程。

入口：[skills/olah-style-journal/SKILL.md](skills/olah-style-journal/SKILL.md)

## 本地构建与检查

需要 Python 3.11+：

~~~bash
git clone https://github.com/1998x-stack/xm-journal.git
cd xm-journal

python -m pip install -r requirements-dev.txt
python -m playwright install chromium

python -m pytest -q
python scripts/build_site.py
python scripts/validate_site.py
python scripts/browser_qa.py

cd _site
python -m http.server 8000
~~~

访问 http://localhost:8000/。

## 自动发布

GitHub Actions 仅在本仓库内容变更或手动触发时：

1. 运行测试；
2. 构建文章首页和静态页面；
3. 校验 HTML、SVG 和本地资源；
4. 使用 Chromium 检查文章的桌面、平板、手机和打印视图；
5. 将静态网站发布到 GitHub Pages。

不设置定时采集任务，不访问其他仓库，不收集 Commit、PR、CI 或部署活动数据。

## 内容边界

- 不把口述变成流水账；要保留细节，同时提炼清晰主线。
- 不虚构经历、数量、成果、动机和因果关系。
- 不强行给每件小事配图；每张图都必须帮助理解。
- 不追踪其他仓库的代码变更，也不将代码活动写进个人日报。
- 不生成自动周报、月报或项目绩效统计。
- GitHub 只作为内容版本库和网站发布平台。

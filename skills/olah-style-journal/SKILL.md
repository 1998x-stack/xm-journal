---
name: olah-style-journal
description: Turn a user's natural spoken daily reflections into a faithful, visually explanatory, responsive and lightly interactive HTML journal article, using progressive narrative, original SVG, semantic HTML and real browser QA.
---

# Olah-style Journal

**先理解这一天，再设计这篇文章。** 本 Skill 将用户自然口述的日常经历、工作反馈、学习过程、感悟、困惑和计划，转化为一篇可独立阅读的视觉日志。目标不是把语音逐字排版，也不是生成任务看板，而是帮助用户看清这一天真正发生了什么、为什么重要，以及下一步如何行动。

本 Skill 继承 [Olah-style-posts](https://github.com/1998x-stack/Olah-style-posts) 的渐进式叙事、图解先行、语义 HTML、原创 SVG、轻量交互和浏览器 QA 方法；论文研究步骤已替换为口述内容理解与个人认知复盘。

## 何时使用

- 用户用语音、口述转写或自然语言描述一天的经历和想法。
- 用户要求整理日报、个人复盘、学习日志、生活习惯记录或阶段感悟。
- 用户希望把已有 Markdown 日志改造成 Olah 风格的独立 HTML 页面。
- 用户要求把一个复杂的想法、决策或习惯回路做成可视化解释。

不要用本 Skill 生成跨仓库工程活动日报、Commit/PR/CI 仪表盘或项目绩效报告。

## 输入与输出

**输入**
- 用户的口述或转写文本。
- 日期（若未提供，使用对话中明确的日期；不能臆造）。
- 可选上下文、受众、希望强调的主题和隐私限制。

**输出**
- journal/daily/YYYY/MM/YYYY-MM-DD.md：结构化的文字原稿。
- posts/YYYY/MM/YYYY-MM-DD/index.html：独立的视觉文章。
- posts/YYYY/MM/YYYY-MM-DD/assets/*.svg：本篇文章独有的原创图解。
- posts/YYYY/MM/YYYY-MM-DD/evidence.json：用户陈述与编辑性归纳的来源记录。
- 首页自动发现的文章卡片。
- 静态校验与浏览器 QA 结果。

## 设计哲学

### 1. 真实优先于完整

- 用户说过的才是事实；没有说过的内容不能为了文章完整而补造。
- 保留具体场景、细节、情绪和语言习惯；只删除无意义的重复口头语。
- 区分事实、感受、解释、猜测、决定、计划和待研究问题。
- 不把 AI 推断包装成用户亲历，也不把未来计划写成已完成。
- 对不确定的日期、人物、数量和因果关系，明确保留未知。

### 2. 一天只抓一条主线

先找出一个最值得回看的认知张力，例如：
- 想做得更多，但行动启动困难；
- AI 提高产出，却降低了过程控制感；
- 知识内容越来越多，真正掌握的却不够；
- 反馈很多，但系统没有留下可恢复的状态。

其他经历围绕主线组织。不要机械地把每句话变成一个标题。

### 3. Olah 式渐进解释

采用以下叙事顺序：

真实场景 → 具体摩擦 → 关键问题 → 心智模型 → 视觉解释 → 个人洞察 → 可执行行动

先让读者理解发生了什么，再展示抽象规律。复杂概念通过局部图解逐步展开，不要一上来堆出整张大图。

### 4. 图解必须解释内容

每张图先写出要回答的问题，再设计 SVG：
- 时间线：一天的节奏、事件和转折；
- 流程图：反馈、决策、恢复路径；
- 关系图：原因、影响、约束和依赖；
- 循环图：习惯、学习、复盘和行动；
- 状态图：一个想法如何逐步变成能力。

每篇文章应根据当天内容选择不同的视觉语言，不要复用同一封面或套用无意义的卡片墙。

## 强制工作流程

### Gate 0 — 阅读仓库规范与示例

1. 阅读根目录 AGENTS.md。
2. 阅读本文件和 [spoken-input-processing.md](references/spoken-input-processing.md)。
3. 检查最近几篇日志的视觉表达，避免重复封面、图解和叙事。
4. 不访问其他 GitHub 仓库收集提交或工程活动。

### Gate 1 — 解析口述

按照 [spoken-input-processing.md](references/spoken-input-processing.md) 建立内容地图：
- 时间线与场景；
- 关键人物/协作关系（只记录必要信息）；
- 事实、感受、判断、疑问、决定和计划；
- 反复出现的摩擦；
- 最值得保留的一条主线。

如果原话存在关键歧义且影响事实，不要自行猜测；只问一个最关键的问题。其他轻微缺口保留为未知。

### Gate 2 — 先写叙事，再画图

先完成文章大纲：
1. 标题：抓住认知变化，不写成泛泛的“今日总结”。
2. 开场：一个真实细节或当天最明显的矛盾。
3. 背景：解释读者需要知道的上下文。
4. 展开：2–5 个主题，每节只回答一个问题。
5. 心智模型：把核心关系压缩成一张图。
6. 反思：区分用户原话与编辑性提炼。
7. 行动：写出用户明确提出的下一步。

阅读 [narrative-architecture.md](references/narrative-architecture.md)。

### Gate 3 — 绘制原创 SVG

遵循 [svg-production.md](references/svg-production.md)：
- SVG 必须有 xmlns、viewBox、title 和 desc；
- 每张图使用独立且唯一的 ID；
- 颜色语义一致，文字可读，关系准确；
- 图注说明这张图揭示了什么；
- 复杂机制拆成多个局部视图，而不是压缩成一张拥挤大图；
- 保存独立 SVG 文件，并在文章中提供有意义的 alt 文本。

### Gate 4 — 生成语义 HTML

从 assets/templates/article.html 和 assets/css/article.css 开始，或按文章需求独立设计：
- 一个 H1，标题层级连续；
- 使用 main、article、nav、section、figure、figcaption；
- 桌面端可用目录导航，手机端自然堆叠；
- CSS 和 JS 本地化，无 CDN、远程字体或分析脚本；
- 打印时移除不必要的交互控件；
- 不在文章正文中展示构建过程、AI 工具或格式宣传。

### Gate 5 — 添加有意义的交互

阅读 [implementation-and-interactivity.md](references/implementation-and-interactivity.md)。

交互只在能帮助理解时加入，例如：
- 按步骤查看某个习惯或认知闭环；
- 切换决策分支并观察结果；
- 展开一个过程中的状态变化；
- 对比行动前后的思维模型。

每个控件都要有默认状态、键盘可操作性和可见反馈。静态图与文字必须在 JavaScript 失效时仍能解释核心内容。

### Gate 6 — 来源与隐私检查

阅读 [evidence-and-citation.md](references/evidence-and-citation.md)：
- 用户陈述标为 user-statement；
- 编辑归纳标为 editorial-synthesis；
- 外部事实只有在确实需要且经过核实时才引用；
- 删除密码、令牌、私人联系方式和未经授权的第三方信息；
- 不伪造证据、数量或外部来源。

### Gate 7 — 质量验证

运行：

~~~bash
python skills/olah-style-journal/scripts/validate.py posts/YYYY/MM/YYYY-MM-DD/index.html
python scripts/build_site.py
python scripts/validate_site.py
python skills/olah-style-journal/scripts/browser_check.py posts/YYYY/MM/YYYY-MM-DD/index.html --output _qa/YYYY-MM-DD
~~~

或使用 python scripts/browser_qa.py 对所有文章执行 Chromium 检查。必须检查 1440px 桌面、768px 平板、390px 和 360px 手机、打印视图、图片加载、SVG 尺寸、控制台错误、交互状态和横向溢出。未执行的检查标为 NOT VERIFIED。

### Gate 8 — 发布

1. 确认 Markdown 原稿、HTML、SVG、来源记录和首页卡片一致。
2. 运行全部测试与质量检查。
3. 提交内容到仓库。
4. 由 main 分支 Pages 工作流构建和发布。
5. 只有 GitHub Actions 部署成功后才报告部署成功；不要把提交成功等同于网站上线。

## 硬性约束

- 不编造用户没有说过的经历、数字、成果、情绪、动机或因果关系。
- 不把“生成了内容”写成“已经掌握知识”。
- 不把“计划做”写成“已经完成”。
- 不把每日口述日志改造成 Commit、PR、CI、部署活动统计。
- 不访问其他仓库采集代码变更或项目活动。
- 不复制 Christopher Olah 或 The Annotated Transformer 的图像、文字、代码和品牌资产。
- 不用图表数量衡量文章质量；每张图都必须回答一个问题。
- 不用自动播放、闪烁或纯装饰交互。
- 不在缺少浏览器证据时声称浏览器 QA 通过。

## 参考资料路由

| 需要 | 文档 |
|---|---|
| 口述内容解析与事实边界 | [spoken-input-processing.md](references/spoken-input-processing.md) |
| 叙事顺序与心智模型 | [narrative-architecture.md](references/narrative-architecture.md) |
| 来源与编辑归纳 | [evidence-and-citation.md](references/evidence-and-citation.md) |
| HTML / CSS 设计规范 | [html-design-system.md](references/html-design-system.md) |
| SVG 生产与校验 | [svg-production.md](references/svg-production.md) |
| 交互设计 | [implementation-and-interactivity.md](references/implementation-and-interactivity.md) |
| 数学公式（需要时） | [math-typesetting.md](references/math-typesetting.md) |
| 浏览器 QA | [browser-qa.md](references/browser-qa.md) |
| 内容评分 | [scorecard.md](references/scorecard.md) |
| 风格来源与版权边界 | [source-notes.md](references/source-notes.md) |
| 发布 | [publishing.md](references/publishing.md) |

## 示例调用

~~~text
请按照 xm-journal 的 AGENTS.md 和 olah-style-journal Skill，
把我刚才口述的今天经历整理成每日 Markdown 原稿，
提炼最重要的一条认知主线，制作原创 SVG 和有意义的交互，
生成独立 HTML，运行静态与浏览器 QA，并发布到 GitHub Pages。
不要追踪任何其他仓库的 Commit、PR 或 CI 活动。
~~~

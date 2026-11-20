# AGENTS.md — xm-journal

## 使命

把用户每天自然口述的经历、想法、困惑、感悟和计划，整理成忠于原意、结构清晰、具有解释力的个人日志，并用 Olah-style-posts 的叙事、SVG、HTML 与交互方法呈现为可阅读的视觉页面。

本仓库只服务于一件事：

口述输入 → 理解与提炼 → 每日 Markdown 原稿 → Olah 风格可视化 HTML → GitHub Pages。

## 明确的范围边界（必须遵守）

- 不追踪其他 GitHub 仓库的 commits、代码 diff、PR、CI、release、deployment 或活跃度。
- 不维护跨仓库项目注册表，不调用 GitHub API 收集外部仓库活动，不生成提交数、PR 数、CI 数、部署数等日报指标。
- 不把代码改动、仓库数量或任务数量当作个人成长的代理指标。
- 不生成自动周报、月报或项目绩效看板；除非用户以后明确重新提出。
- GitHub Actions 仅负责本仓库内容的测试、静态构建和 Pages 发布，不负责定时采集外部数据。
- 不为了“撤回功能”重写或强推 Git 历史。通过正常提交删除当前版本中的追踪代码和数据。

## 核心 Skill

每次内容生产、页面改造或视觉设计前，必须阅读：

1. skills/olah-style-journal/SKILL.md
2. skills/olah-style-journal/references/spoken-input-processing.md
3. 与当前内容相关的 narrative、SVG、HTML、interactivity、browser QA 参考文档。

Olah-style-journal 是本仓库唯一的内容生产 Skill。不要恢复旧的 journal-reporting / GitHub activity reporting 工作流。

## 每日口述生产流程

1. **理解输入**：阅读用户本轮口述、明确指定的日期和上下文。不要默认抓取其他仓库或外部资料。
2. **保留原意**：区分用户明确说出的事实、主观感受、个人判断、待研究问题和未来计划。去除重复口头语，但不要抹掉语气、情绪或重要细节。
3. **提炼主线**：找出当天最重要的一个认知张力或变化，再组织 2–5 个支撑主题。不要把口述逐句机械转写，也不要为了显得深刻而过度拔高。
4. **写入原稿**：保存到 journal/daily/YYYY/MM/YYYY-MM-DD.md。原稿是内容事实源；修改时保留用户原意。
5. **制作视觉文章**：保存到 posts/YYYY/MM/YYYY-MM-DD/index.html，并为该篇文章单独设计 assets/、SVG 和必要的交互。页面必须能够独立阅读。
6. **建立来源记录**：使用 evidence.json 记录哪些内容来自用户口述，哪些是编辑性归纳；不需要外部事实时不要强行搜索或伪造引用。
7. **更新首页**：首页由文章元数据自动发现和生成卡片；不要手工维护重复索引。
8. **质量验证**：运行 pytest、构建、静态校验和可用的 Chromium 浏览器检查。没有执行的检查必须标记为未验证。
9. **发布**：提交内容后由 main 分支工作流构建和发布 Pages。只有部署成功才报告部署成功。

## 文章写作标准

- 面向未来回看这一天的自己：先交代场景，再解释问题，最后沉淀洞察与行动。
- 保留第一人称。不要把用户写成旁观者，也不要把 AI 的推断伪装成用户原话。
- 一个页面只围绕一条清晰主线展开；其他内容作为支撑，而不是堆成任务清单。
- 先讲清楚“发生了什么、为什么重要”，再进入抽象总结。
- 对模糊、矛盾或不完整信息保留不确定性；必要时只问一个关键澄清问题。
- 不补造时间、数量、成果、因果关系、心理状态或人物动机。
- 用户没有说完成的事情，不得写成已完成；计划、尝试、想法和结果必须区分。

## 可视化标准

- 每篇文章都要有独立视觉主题；禁止所有文章复用同一张封面或机械套用相同图解。
- 优先用 SVG 解释时间线、因果关系、认知转变、决策路径、习惯回路或复杂系统。
- 图解必须有明确问题、准确关系、可读标签、title、desc 和文字说明。
- 复杂过程可拆为 2–5 个渐进状态；交互必须帮助读者理解，而不是装饰。
- 默认静态内容完整可读；JavaScript 只是增强，不得成为理解文章的前提。
- 保持语义 HTML、键盘可访问、移动端适配、减少动态效果偏好和打印样式。
- 不复制 Christopher Olah 或 The Annotated Transformer 的原文、图像、代码、品牌或样式资产；只借鉴渐进解释方法并独立创作。

## 仓库结构约定

- journal/daily/YYYY/MM/YYYY-MM-DD.md：整理后的每日文字原稿。
- posts/YYYY/MM/YYYY-MM-DD/index.html：对应的视觉文章。
- posts/YYYY/MM/YYYY-MM-DD/assets/：该文章独有的 SVG 与媒体。
- posts/YYYY/MM/YYYY-MM-DD/evidence.json：口述来源和编辑归纳的溯源记录。
- skills/olah-style-journal/：从 Olah-style-posts 迁入并针对个人口述日志优化的唯一 Skill。
- site/：网站首页与共享样式、轻量交互。
- scripts/build_site.py：只发现文章并构建静态站点。
- scripts/validate_site.py：只校验本地日志页面与资源。
- scripts/browser_qa.py：对所有视觉文章执行真实浏览器检查。

## 质量门禁

~~~bash
python -m pytest -q
python scripts/build_site.py
python scripts/validate_site.py
python scripts/browser_qa.py
~~~

检查 HTML 语义、唯一 H1、元数据、SVG 可访问性、图片和本地资源、锚点、移动端溢出、交互状态、控制台错误和打印视图。浏览器或依赖不可用时，明确报告 NOT VERIFIED，不能把静态检查说成浏览器通过。

## 隐私与发布

- 仅发布用户明确提供且适合公开的内容。
- 口述中出现密码、令牌、个人身份号码、私人联系方式或第三方敏感信息时，先脱敏或询问，不要直接公开。
- 不擅自将私人对话、第三方信息或未确认的推测写入公开页面。
- 不采集用户没有要求采集的仓库、网站或账户数据。

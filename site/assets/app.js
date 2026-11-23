/* Browse spoken journal entries by topic, date and consecutive seven-day windows. */
(() => {
  const grid = document.querySelector("#post-grid");
  const search = document.querySelector("#search-input");
  const category = document.querySelector("#category-filter");
  const dateFrom = document.querySelector("#date-from");
  const dateTo = document.querySelector("#date-to");
  const reset = document.querySelector("#reset-filters");
  const empty = document.querySelector("#empty-state");
  const summary = document.querySelector("#results-summary");
  const pagination = document.querySelector("#pagination");
  const newer = document.querySelector("#page-newer");
  const older = document.querySelector("#page-older");
  const indicator = document.querySelector("#page-indicator");
  const range = document.querySelector("#page-range");

  if (![grid, search, category, dateFrom, dateTo, reset, empty, summary,
    pagination, newer, older, indicator, range].every(Boolean)) return;

  // UTC day indexes avoid DST and browser-timezone shifts when calculating calendar days.
  const DAY = 24 * 60 * 60 * 1000;
  function dayIndex(iso) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(iso)) return NaN;
    const [year, month, day] = iso.split("-").map(Number);
    const utc = Date.UTC(year, month - 1, day);
    const valid = new Date(utc).toISOString().slice(0, 10) === iso;
    return valid ? utc / DAY : NaN;
  }
  function dayLabel(index) {
    return new Date(index * DAY).toISOString().slice(0, 10).replaceAll("-", ".");
  }

  // The site generator has already ordered entries newest first.
  const cards = [...grid.querySelectorAll(".post-card")]
    .map(node => ({node, day: dayIndex(node.dataset.date || "")}))
    .filter(item => Number.isFinite(item.day))
    .sort((a, b) => b.day - a.day);
  let page = 0;

  if (cards.length === 0) {
    summary.textContent = "尚无可浏览的日志";
    return;
  }

  function render() {
    const keyword = search.value.trim().toLocaleLowerCase();
    const topic = category.value;
    const from = dateFrom.value ? dayIndex(dateFrom.value) : -Infinity;
    const to = dateTo.value ? dayIndex(dateTo.value) : Infinity;
    const invalidRange = from > to;
    const filtered = invalidRange ? [] : cards.filter(({node, day}) =>
      (!keyword || (node.dataset.search || "").includes(keyword)) &&
      (!topic || node.dataset.category === topic) &&
      day >= from && day <= to
    );

    if (filtered.length === 0) {
      cards.forEach(({node}) => { node.hidden = true; });
      empty.hidden = false;
      empty.textContent = invalidRange
        ? "开始日期不能晚于结束日期，请调整时间范围。"
        : "没有找到匹配的日志，请调整主题、日期或关键词。";
      pagination.hidden = true;
      summary.textContent = invalidRange ? "日期范围无效" : "筛选结果：0 篇日志";
      return;
    }

    // One page means exactly seven consecutive calendar days, not seven cards.
    // The first window ends on the most recent matching journal date.
    const newest = filtered[0].day;
    const oldest = filtered[filtered.length - 1].day;
    const totalPages = Math.floor((newest - oldest) / 7) + 1;
    page = Math.min(page, totalPages - 1);
    const end = newest - 7 * page;
    const start = end - 6;
    const visible = new Set(filtered.filter(({day}) => day >= start && day <= end)
      .map(({node}) => node));
    cards.forEach(({node}) => { node.hidden = !visible.has(node); });

    empty.hidden = visible.size !== 0;
    if (!empty.hidden) {
      empty.textContent = "这七天还没有日志，可以翻到其他时间段继续阅读。";
    }

    summary.textContent = `筛选结果：${filtered.length} 篇 · 本页 ${visible.size} 篇`;
    indicator.textContent = `第 ${page + 1} / ${totalPages} 页`;
    range.textContent = `${dayLabel(start)} — ${dayLabel(end)}（7 天）`;
    newer.disabled = page === 0;
    older.disabled = page >= totalPages - 1;
    pagination.hidden = false;
  }

  function resetPage() {
    page = 0;
    render();
  }
  search.addEventListener("input", resetPage);
  category.addEventListener("change", resetPage);
  dateFrom.addEventListener("change", resetPage);
  dateTo.addEventListener("change", resetPage);

  reset.addEventListener("click", () => {
    search.value = "";
    category.value = "";
    dateFrom.value = "";
    dateTo.value = "";
    resetPage();
  });
  newer.addEventListener("click", () => {
    if (page > 0) { page -= 1; render(); }
  });
  older.addEventListener("click", () => {
    if (!older.disabled) { page += 1; render(); }
  });
  render();
})();

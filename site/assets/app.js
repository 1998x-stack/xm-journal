(() => {
  const grid = document.querySelector("#post-grid");
  const search = document.querySelector("#search-input");
  const category = document.querySelector("#category-filter");
  const count = document.querySelector("#post-count");
  const empty = document.querySelector("#empty-state");
  if (!grid || !search || !category) return;

  const cards = [...grid.querySelectorAll(".post-card")];
  function filterPosts() {
    const query = search.value.trim().toLocaleLowerCase();
    const selected = category.value;
    let visible = 0;
    for (const card of cards) {
      const matchesQuery = !query || (card.dataset.search || "").includes(query);
      const matchesCategory = !selected || card.dataset.category === selected;
      const show = matchesQuery && matchesCategory;
      card.hidden = !show;
      if (show) visible += 1;
    }
    if (count) count.textContent = String(visible);
    if (empty) empty.hidden = visible !== 0;
  }

  search.addEventListener("input", filterPosts);
  category.addEventListener("change", filterPosts);
  filterPosts();
})();

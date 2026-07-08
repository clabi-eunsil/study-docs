// Category/Tags 컬럼이 있는 표(용어집)에 클릭형 필터를 붙인다.
// 소스 repo의 GLOSSARY.md 형식을 그대로 이용하므로, 콘텐츠 쪽은 손댈 필요가 없다.
(function () {
  function textOf(cell) {
    return cell ? cell.textContent.trim() : "";
  }

  function buildFilter(table) {
    var headerCells = table.querySelectorAll("thead th");
    if (!headerCells.length) return;

    var headers = Array.prototype.map.call(headerCells, textOf);
    var categoryIdx = headers.indexOf("Category");
    var tagsIdx = headers.indexOf("Tags");
    if (categoryIdx === -1 || tagsIdx === -1) return;

    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    if (!rows.length) return;

    var categories = new Set();
    var tags = new Set();
    rows.forEach(function (row) {
      var cells = row.children;
      var cat = textOf(cells[categoryIdx]);
      if (cat) categories.add(cat);
      textOf(cells[tagsIdx]).split(",").forEach(function (t) {
        t = t.trim();
        if (t) tags.add(t);
      });
    });

    var active = new Set();
    var bar = document.createElement("div");
    bar.className = "glossary-filter";

    var countEl = document.createElement("span");
    countEl.className = "glossary-filter__count";

    function applyFilter() {
      var shown = 0;
      rows.forEach(function (row) {
        var cells = row.children;
        var cat = textOf(cells[categoryIdx]);
        var rowTags = textOf(cells[tagsIdx]).split(",").map(function (t) {
          return t.trim();
        });
        var visible =
          active.size === 0 ||
          active.has("cat:" + cat) ||
          rowTags.some(function (t) {
            return active.has("tag:" + t);
          });
        row.style.display = visible ? "" : "none";
        if (visible) shown++;
      });
      countEl.textContent = shown + " / " + rows.length + "개 표시 중";
    }

    function makeChip(label, key) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.className = "glossary-filter__chip";
      chip.textContent = label;
      chip.addEventListener("click", function () {
        if (active.has(key)) {
          active.delete(key);
          chip.classList.remove("glossary-filter__chip--active");
        } else {
          active.add(key);
          chip.classList.add("glossary-filter__chip--active");
        }
        applyFilter();
      });
      return chip;
    }

    function makeGroup(label, values, prefix) {
      var group = document.createElement("div");
      group.className = "glossary-filter__group";
      var groupLabel = document.createElement("span");
      groupLabel.className = "glossary-filter__label";
      groupLabel.textContent = label;
      group.appendChild(groupLabel);
      Array.from(values)
        .sort()
        .forEach(function (v) {
          group.appendChild(makeChip(v, prefix + v));
        });
      return group;
    }

    var resetBtn = document.createElement("button");
    resetBtn.type = "button";
    resetBtn.className = "glossary-filter__reset";
    resetBtn.textContent = "전체 보기";
    resetBtn.addEventListener("click", function () {
      active.clear();
      bar.querySelectorAll(".glossary-filter__chip--active").forEach(function (c) {
        c.classList.remove("glossary-filter__chip--active");
      });
      applyFilter();
    });

    bar.appendChild(makeGroup("카테고리", categories, "cat:"));
    bar.appendChild(makeGroup("태그", tags, "tag:"));
    bar.appendChild(resetBtn);
    bar.appendChild(countEl);

    table.parentNode.insertBefore(bar, table);
    applyFilter();
  }

  function init() {
    document.querySelectorAll("article table").forEach(buildFilter);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

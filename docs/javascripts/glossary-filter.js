// GLOSSARY.md는 항상 "Category | 설명" 표(카테고리 인덱스)가 먼저 나오고
// 그 아래 "Term | ... | Category | ... " 표(전체 용어)가 이어진다.
// 인덱스 표의 카테고리 이름을 클릭하면 아래 용어 표를 그 카테고리로 필터링한다.
// 태그 기반 필터는 태그 수가 너무 많아 오히려 산만해서 카테고리만 남겼다.
(function () {
  function textOf(cell) {
    return cell ? cell.textContent.trim() : "";
  }

  function findTables() {
    var tables = document.querySelectorAll("article table");
    var indexTable = null;
    var termsTable = null;

    tables.forEach(function (table) {
      var headers = Array.prototype.map.call(table.querySelectorAll("thead th"), textOf);
      if (headers.length === 2 && headers[0] === "Category" && headers[1] === "설명") {
        indexTable = table;
      } else if (headers.indexOf("Category") !== -1 && headers.indexOf("Term") !== -1) {
        termsTable = table;
      }
    });

    return { indexTable: indexTable, termsTable: termsTable };
  }

  function init() {
    var found = findTables();
    if (!found.indexTable || !found.termsTable) return;

    var indexTable = found.indexTable;
    var termsTable = found.termsTable;

    var termHeaders = Array.prototype.map.call(termsTable.querySelectorAll("thead th"), textOf);
    var categoryIdx = termHeaders.indexOf("Category");
    var termRows = Array.prototype.slice.call(termsTable.querySelectorAll("tbody tr"));
    var indexRows = Array.prototype.slice.call(indexTable.querySelectorAll("tbody tr"));
    if (!termRows.length || !indexRows.length) return;

    var counts = {};
    termRows.forEach(function (row) {
      var cat = textOf(row.children[categoryIdx]);
      counts[cat] = (counts[cat] || 0) + 1;
    });

    var hint = document.createElement("p");
    hint.className = "glossary-filter__hint";
    hint.innerHTML =
      "<em>카테고리를 클릭하면 아래 용어 표가 그 카테고리만 보이도록 좁혀집니다. 다시 클릭하면 전체 보기로 돌아갑니다.</em>";
    indexTable.parentNode.insertBefore(hint, indexTable);

    var activeRow = null;
    var activeCat = null;

    function applyFilter() {
      termRows.forEach(function (row) {
        var cat = textOf(row.children[categoryIdx]);
        row.style.display = !activeCat || cat === activeCat ? "" : "none";
      });
    }

    indexRows.forEach(function (row) {
      var cell = row.children[0];
      var cat = textOf(cell);
      var count = counts[cat] || 0;

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "glossary-filter__cat";
      btn.textContent = cat;

      var badge = document.createElement("span");
      badge.className = "glossary-filter__badge";
      badge.textContent = count;

      cell.textContent = "";
      cell.appendChild(btn);
      cell.appendChild(badge);

      btn.addEventListener("click", function () {
        if (activeRow) {
          activeRow.classList.remove("glossary-filter__row--active");
        }
        if (activeRow === row) {
          activeRow = null;
          activeCat = null;
        } else {
          activeRow = row;
          activeCat = cat;
          row.classList.add("glossary-filter__row--active");
        }
        applyFilter();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

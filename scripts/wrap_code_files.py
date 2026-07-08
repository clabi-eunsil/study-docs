#!/usr/bin/env python3
"""docs/ 아래 코드/설정 파일을 nav에 노출하지 않고, 본문에서 링크된 지점 바로
아래 접이식(pymdownx.details) 블록으로 인라인한다.

이전에는 모든 비-.md 파일을 별도 .md 페이지로 wrap해서 mkdocs nav를 채웠지만,
그러면 requirements.txt/docker-compose.yml 같은 보조 파일까지 학습 콘텐츠와
동급으로 목차에 노출되는 문제가 있었다. 이제는:

- README 등에서 실제로 링크된 코드/설정 파일만 처리 대상으로 삼는다. 별도
  페이지를 만들지 않고, 참조한 md 파일 하단 "코드 보기" 섹션에 접이식 블록으로
  삽입한 뒤 본문 링크는 그 블록으로 점프하는 앵커 링크로 바꾼다.
- 어디서도 링크되지 않는 파일은 페이지를 만들지 않는다(=nav에 안 뜬다).
- 디렉터리를 가리키는 링크는 GitHub 저장소 링크로 바꾼다.
- templates/*.md 같은 학습 기록용 md 파일은 챕터 루트로 끌어올려 references.md
  처럼 목차에 바로 노출되게 한다.
"""
import os
import re
import sys
from pathlib import Path

SKIP_SUFFIXES = {
    ".md", ".markdown",
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp",
}

LANG_BY_NAME = {
    "Dockerfile": "dockerfile",
    "Makefile": "makefile",
}
LANG_BY_SUFFIX = {
    ".py": "python",
    ".sh": "bash",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".toml": "toml",
    ".cfg": "ini",
    ".ini": "ini",
    ".txt": "text",
    ".csv": "text",
    ".env": "bash",
    ".example": "bash",
    ".dockerignore": "text",
    ".gitignore": "text",
}

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
LIST_MARKER_RE = re.compile(r"^(\s*)((?:\d+[.)]|[-*+])\s+)")


def block_end_line(lines: list[str], start: int) -> int:
    """start가 표 또는 목록 항목 줄이면, 그 표/목록 전체가 끝나는 줄
    인덱스를 찾는다(중간에 접이식 블록을 끼워 넣으면 표가 깨지거나
    번호 매기기가 끊기므로, 블록 전체가 끝난 뒤에 끼워 넣기 위함)."""
    line = lines[start]
    if line.lstrip().startswith("|"):
        end = start
        while end + 1 < len(lines) and lines[end + 1].lstrip().startswith("|"):
            end += 1
        return end

    if not LIST_MARKER_RE.match(line):
        return start

    end = start
    i = start + 1
    while i < len(lines):
        cur = lines[i]
        if cur.strip() == "":
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and (LIST_MARKER_RE.match(lines[j]) or lines[j].startswith((" ", "\t"))):
                end = j
                i = j + 1
                continue
            break
        if LIST_MARKER_RE.match(cur) or cur.startswith((" ", "\t")):
            end = i
            i += 1
            continue
        break
    return end


def guess_lang(path: Path) -> str:
    if path.name in LANG_BY_NAME:
        return LANG_BY_NAME[path.name]
    return LANG_BY_SUFFIX.get(path.suffix, "text")


def fence_for(content: str) -> str:
    runs = re.findall(r"`+", content)
    longest = max((len(r) for r in runs), default=0)
    return "`" * max(3, longest + 1)


def slug_for(relpath: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", relpath).strip("-").lower()
    return f"file-{slug}"


def load_sources(root_dir: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    sources_file = root_dir / "sources.txt"
    if not sources_file.exists():
        return sources
    for line in sources_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, url, *_ = line.split("|")
        sources[name.strip()] = url.strip()
    return sources


def repo_web_url(git_url: str) -> str:
    return git_url[:-4] if git_url.endswith(".git") else git_url


def _relink_after_move(content: str, old_dir: Path, new_dir: Path) -> str:
    """파일을 old_dir에서 new_dir로 옮길 때, 그 파일 자신이 담고 있던
    상대 링크를 새 위치 기준으로 다시 계산한다."""

    def repl(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
            return m.group(0)
        path_part, sep, frag = target.partition("#")
        if not path_part:
            return m.group(0)
        absolute = (old_dir / path_part).resolve()
        new_target = Path(os.path.relpath(absolute, new_dir)).as_posix()
        return f"[{label}]({new_target}{sep}{frag})"

    return LINK_RE.sub(repl, content)


def flatten_templates(source_dir: Path) -> None:
    """templates/*.md(학습 기록)를 챕터 루트로 끌어올려 nav에 바로 노출한다."""
    moved_names: set[str] = set()
    for templates_dir in source_dir.rglob("templates"):
        if not templates_dir.is_dir():
            continue
        for md_file in list(templates_dir.glob("*.md")):
            dest = templates_dir.parent / md_file.name
            content = _relink_after_move(
                md_file.read_text(encoding="utf-8"), templates_dir, templates_dir.parent
            )
            md_file.unlink()
            dest.write_text(content, encoding="utf-8")
            moved_names.add(md_file.name)
        try:
            templates_dir.rmdir()
        except OSError:
            pass  # 코드/설정 파일이 남아 있으면 그대로 둔다

    if not moved_names:
        return
    for md_file in source_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        new_text = text
        for name in moved_names:
            new_text = new_text.replace(f"(templates/{name}", f"({name}")
        if new_text != text:
            md_file.write_text(new_text, encoding="utf-8")


def process_source(source_dir: Path, git_url: str) -> None:
    flatten_templates(source_dir)
    repo_web = repo_web_url(git_url)
    source_root = source_dir.resolve()
    to_delete: set[Path] = set()

    for md_file in sorted(source_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        seen: dict[Path, str] = {}
        order: list[Path] = []
        first_prose_line: dict[Path, int] = {}
        first_table_line: dict[Path, int] = {}

        def repl(m: re.Match) -> str:
            label, target = m.group(1), m.group(2)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                return m.group(0)
            path_part, sep, frag = target.partition("#")
            if not path_part:
                return m.group(0)
            resolved = (md_file.parent / path_part).resolve()
            if not resolved.exists():
                return m.group(0)
            try:
                resolved.relative_to(source_root)
            except ValueError:
                return m.group(0)  # source 밖은 건드리지 않는다

            if resolved.is_dir():
                rel = resolved.relative_to(source_root).as_posix()
                return f"[{label}]({repo_web}/tree/main/{rel})"

            if resolved.suffix in SKIP_SUFFIXES:
                return m.group(0)

            if resolved not in seen:
                seen[resolved] = slug_for(resolved.relative_to(source_root).as_posix())
                order.append(resolved)

            # 표 안 셀에는 접이식 블록을 못 끼워 넣으므로, 표가 아닌 첫 등장
            # 위치를 따로 기억해 둔다(표에만 등장하면 표 바로 뒤에 끼워 넣는다).
            line_idx = text.count("\n", 0, m.start())
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.start())
            line_end = len(text) if line_end == -1 else line_end
            if text[line_start:line_end].lstrip().startswith("|"):
                first_table_line.setdefault(resolved, line_idx)
            else:
                first_prose_line.setdefault(resolved, line_idx)

            return f"[{label}](#{seen[resolved]})"

        new_text = LINK_RE.sub(repl, text)

        if order:
            new_lines = new_text.split("\n")
            insertions: dict[int, list[Path]] = {}
            for resolved in order:
                start_line = first_prose_line.get(resolved, first_table_line.get(resolved))
                target_line = block_end_line(new_lines, start_line)
                insertions.setdefault(target_line, []).append(resolved)

            for line_idx in sorted(insertions, reverse=True):
                block: list[str] = []
                for resolved in insertions[line_idx]:
                    try:
                        content = resolved.read_text(encoding="utf-8")
                    except (UnicodeDecodeError, OSError):
                        continue
                    rel_display = Path(os.path.relpath(resolved, md_file.parent)).as_posix()
                    lang = guess_lang(resolved)
                    fence = fence_for(content)
                    fenced = "\n".join([f"{fence}{lang}", *content.splitlines(), fence])
                    admonition_body = ["    " + line if line else "" for line in fenced.splitlines()]
                    block += ["", f'<a id="{seen[resolved]}"></a>', f'??? note "{rel_display}"', *admonition_body]
                    to_delete.add(resolved)
                new_lines[line_idx + 1:line_idx + 1] = block

            new_text = "\n".join(new_lines)

        if new_text != text:
            md_file.write_text(new_text, encoding="utf-8")

    for path in to_delete:
        path.unlink(missing_ok=True)


def main(docs_dir: Path) -> None:
    root_dir = docs_dir.parent
    sources = load_sources(root_dir)
    for name, git_url in sources.items():
        source_dir = docs_dir / name
        if source_dir.is_dir():
            process_source(source_dir, git_url)


if __name__ == "__main__":
    main(Path(sys.argv[1]))

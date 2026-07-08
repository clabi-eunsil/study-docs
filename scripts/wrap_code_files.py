#!/usr/bin/env python3
"""docs/ 아래 코드/설정 파일을 문법 강조가 되는 .md 페이지로 감싼다.

MkDocs는 .md가 아닌 파일을 원본 그대로 복사만 하기 때문에, 별도 페이지로
만들지 않으면 nav에도 안 잡히고 문법 강조도 되지 않는다.
"""
import re
import sys
from pathlib import Path

SKIP_SUFFIXES = {
    ".md", ".markdown",
    ".svg", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp",
}
SKIP_NAMES = {".DS_Store"}

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


def guess_lang(path: Path) -> str:
    if path.name in LANG_BY_NAME:
        return LANG_BY_NAME[path.name]
    return LANG_BY_SUFFIX.get(path.suffix, "text")


def fence_for(content: str) -> str:
    runs = re.findall(r"`+", content)
    longest = max((len(r) for r in runs), default=0)
    return "`" * max(3, longest + 1)


def wrap_file(path: Path) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return

    lang = guess_lang(path)
    fence = fence_for(content)
    md_path = path.with_name(path.name + ".md")
    rel_title = path.name

    md_path.write_text(
        f"# {rel_title}\n\n{fence}{lang}\n{content}\n{fence}\n",
        encoding="utf-8",
    )
    # 원본과 이름이 같은 디렉터리를 만들어내 mkdocs 출력 경로가 충돌하므로 원본은 지운다.
    path.unlink()


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")


def rewrite_links(docs_dir: Path) -> None:
    """감싸면서 사라진 원본 파일을 가리키던 상대링크를 <file>.md로 고쳐준다."""
    for md_file in docs_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")

        def repl(m: re.Match) -> str:
            label, target = m.group(1), m.group(2)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:|^#", target):
                return m.group(0)
            path_part, sep, frag = target.partition("#")
            if not path_part:
                return m.group(0)
            resolved = (md_file.parent / path_part).resolve()
            if resolved.exists():
                return m.group(0)
            candidate = resolved.parent / (resolved.name + ".md")
            if not candidate.exists():
                return m.group(0)
            new_target = path_part + ".md" + (sep + frag if sep else "")
            return f"[{label}]({new_target})"

        new_text = LINK_RE.sub(repl, text)
        if new_text != text:
            md_file.write_text(new_text, encoding="utf-8")


def main(docs_dir: Path) -> None:
    for path in docs_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        wrap_file(path)
    rewrite_links(docs_dir)


if __name__ == "__main__":
    main(Path(sys.argv[1]))

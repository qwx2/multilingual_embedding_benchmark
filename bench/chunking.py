"""Header-aware Markdown chunking.

One chunk per `##` section, plus one for any preamble between the `#` title and the first
`##`. Each chunk's embedded text is prefixed with the document title and section heading so a
chunk still says what it is about when read on its own.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

INTRO = "(intro)"


@dataclass(frozen=True)
class Chunk:
    id: str  # "<doc>#<section-slug>" -- stable, human-readable, used as the eval label
    doc: str  # file stem, e.g. "zakat"
    title: str  # the document's H1
    section: str  # the H2 heading, or INTRO
    body: str

    @property
    def text(self) -> str:
        """The string that gets embedded."""
        if self.section == INTRO:
            return f"{self.title}\n\n{self.body}"
        return f"{self.title}\n## {self.section}\n\n{self.body}"


def slugify(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def chunk_markdown(doc: str, markdown: str) -> list[Chunk]:
    title = doc
    sections: list[tuple[str, list[str]]] = [(INTRO, [])]
    in_fence = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("# "):
            title = line[2:].strip()
            continue
        if not in_fence and line.startswith("## "):
            sections.append((line[3:].strip(), []))
            continue
        sections[-1][1].append(line)

    chunks = []
    for section, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        slug = "intro" if section == INTRO else slugify(section)
        chunks.append(Chunk(f"{doc}#{slug}", doc, title, section, body))

    ids = [c.id for c in chunks]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{doc}: two sections slugify to the same id: {ids}")
    return chunks


def load_corpus(knowledge_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        chunks.extend(chunk_markdown(path.stem, path.read_text(encoding="utf-8")))
    return chunks

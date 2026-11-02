"""Document loading and corpus management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    """A single document in the corpus."""

    doc_id: str
    title: str
    content: str
    path: Path

    def __repr__(self) -> str:
        return f"Document(doc_id={self.doc_id!r}, title={self.title!r})"


def load_corpus(corpus_dir: str | Path) -> list[Document]:
    """Load all .txt documents from corpus_dir.

    Each file's stem becomes the doc_id.
    The first non-empty line of the file becomes the title.
    Documents are returned sorted by doc_id.
    """
    corpus_dir = Path(corpus_dir)
    if not corpus_dir.is_dir():
        raise ValueError(f"Corpus directory not found: {corpus_dir}")

    documents: list[Document] = []
    for path in sorted(corpus_dir.glob("*.txt")):
        content = path.read_text(encoding="utf-8")
        lines = [line.strip() for line in content.splitlines()]
        title = next((line for line in lines if line), path.stem)
        documents.append(
            Document(
                doc_id=path.stem,
                title=title,
                content=content,
                path=path,
            )
        )

    return documents

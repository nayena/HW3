"""Command-line interface for the search engine."""

from __future__ import annotations

import os
from pathlib import Path

import click

from searchengine.corpus import load_corpus
from searchengine.normalize import normalize_document, normalize_query
from searchengine.search import SearchEngine


def _locate_corpus() -> Path:
    """Find the corpus directory: env var, then repo-relative default."""
    if env := os.environ.get("SEARCHENGINE_CORPUS"):
        return Path(env)
    candidates = [
        Path(__file__).parent.parent.parent / "corpus" / "docs",
        Path("corpus") / "docs",
        Path("corpus"),
    ]
    for c in candidates:
        if c.is_dir():
            return c
    raise click.ClickException(
        "Cannot locate corpus directory. "
        "Set SEARCHENGINE_CORPUS or run from the project root."
    )


@click.group()
def cli() -> None:
    """A small search engine for exploring normalization and testing."""


@cli.command()
@click.argument("query")
@click.option("--top-k", default=5, show_default=True, help="Maximum results to return.")
@click.option("--corpus", default=None, help="Path to corpus directory.")
def search(query: str, top_k: int, corpus: str | None) -> None:
    """Search the document corpus for QUERY."""
    corpus_dir = Path(corpus) if corpus else _locate_corpus()
    docs = load_corpus(corpus_dir)
    if not docs:
        click.echo("No documents found in corpus.")
        return

    engine = SearchEngine(docs)
    results = engine.search(query, top_k=top_k)

    if not results:
        click.echo(f"No results for: {query!r}")
        return

    click.echo(f"Results for: {query!r}\n")
    for i, r in enumerate(results, 1):
        click.echo(f"  {i}. {r.title}")
        click.echo(f"     {r.snippet}")
        click.echo()


@cli.command(name="list-docs")
@click.option("--corpus", default=None, help="Path to corpus directory.")
def list_docs(corpus: str | None) -> None:
    """List all documents in the corpus."""
    corpus_dir = Path(corpus) if corpus else _locate_corpus()
    docs = load_corpus(corpus_dir)
    click.echo(f"Corpus: {corpus_dir}  ({len(docs)} documents)\n")
    for doc in docs:
        click.echo(f"  [{doc.doc_id}]  {doc.title}")


@cli.command()
@click.argument("text")
def explain(text: str) -> None:
    """Show how TEXT is normalized for documents vs. queries."""
    click.echo(f"Input:             {text!r}")
    click.echo(f"Document tokens:   {normalize_document(text)}")
    click.echo(f"Query tokens:      {normalize_query(text)}")
    consistent = normalize_document(text) == normalize_query(text)
    click.echo(f"Consistent:        {consistent}")

from __future__ import annotations

import re
from pathlib import Path

from voice_agent_app.models import KnowledgeArticle

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]{2,}")


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_PATTERN.findall(text)}


def load_knowledge(root: Path) -> list[KnowledgeArticle]:
    knowledge_dir = root / "data" / "knowledge"
    articles: list[KnowledgeArticle] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        header, _, body = raw.partition("\n\n")
        metadata: dict[str, str] = {}
        for line in header.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", maxsplit=1)
            metadata[key.strip().lower()] = value.strip()
        content = body.strip()
        articles.append(
            KnowledgeArticle(
                article_id=path.stem,
                title=metadata.get("title", path.stem),
                topic=metadata.get("topic", "support"),
                content=content,
                keywords=frozenset(tokenize(content + " " + metadata.get("title", ""))),
            )
        )
    return articles


class KnowledgeBase:
    def __init__(self, articles: list[KnowledgeArticle]) -> None:
        self.articles = articles

    def search(self, query: str, limit: int = 2) -> list[KnowledgeArticle]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        ranked = sorted(
            self.articles,
            key=lambda article: len(query_tokens & article.keywords),
            reverse=True,
        )
        return [article for article in ranked[:limit] if query_tokens & article.keywords]

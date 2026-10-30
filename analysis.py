"""Small, deterministic text analysis functions used by the workshop."""

import re
from collections import Counter
from pathlib import Path


def tokenize(text: str) -> list[str]:
    """Extract case-insensitive Unicode words from raw text.

    Letters and internal apostrophes are retained. Numbers and underscores
    separate words. Markdown links, code and markup are not removed.

    :param text: Text to analyze.
    :returns: Lowercase words in their original order.
    """
    normalized = text.casefold().replace("’", "'").replace("ʼ", "'")
    return re.findall(r"[^\W\d_]+(?:'[^\W\d_]+)*", normalized)


def analyze_text(text: str, top: int = 10) -> dict:
    """Count words and select the most frequent ones.

    Ties are sorted alphabetically for deterministic output. An empty text
    has zero words. Common words are included; no stop-word list is applied.

    :param text: Raw input text, including any Markdown syntax.
    :param top: Positive number of frequent words to include.
    :returns: Total count, unique count and a list of frequent words.
    :raises ValueError: If top is not a positive integer.
    """
    if isinstance(top, bool) or not isinstance(top, int) or top < 1:
        raise ValueError("top must be a positive integer")
    words = tokenize(text)
    counts = Counter(words)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return {
        "total_words": len(words),
        "unique_words": len(counts),
        "top_words": [
            {"word": word, "count": count} for word, count in ranked[:top]
        ],
    }


def analyze_file(path: Path, top: int = 10) -> dict:
    """Read a UTF-8 document and attach its filename to the statistics.

    :param path: Path of an existing UTF-8 text file.
    :param top: Number of frequent words to include.
    :returns: A versioned record suitable for JSON serialization.
    :raises OSError: If the file cannot be read.
    :raises UnicodeError: If the input is not UTF-8.
    :raises ValueError: If top is invalid.
    """
    text = path.read_text(encoding="utf-8-sig")
    return {"schema_version": 1, "source": path.name, **analyze_text(text, top)}

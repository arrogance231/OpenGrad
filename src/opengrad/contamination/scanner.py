import hashlib
import re
from collections.abc import Iterable


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def exact_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode()).hexdigest()


def exact_overlap(left: Iterable[str], right: Iterable[str]) -> set[str]:
    rhs = {exact_hash(x) for x in right}
    return {exact_hash(x) for x in left if exact_hash(x) in rhs}


def json_schema_signature(value: object) -> str:
    import json

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def ngrams(text: str, n: int = 5) -> set[str]:
    text = normalize(text)
    return {text[i : i + n] for i in range(max(0, len(text) - n + 1))}


def jaccard(left: str, right: str, n: int = 5) -> float:
    a, b = ngrams(left, n), ngrams(right, n)
    return len(a & b) / len(a | b) if a | b else 1.0


def edit_similarity(left: str, right: str) -> float:
    from difflib import SequenceMatcher

    return SequenceMatcher(None, normalize(left), normalize(right)).ratio()


def minhash_signature(text: str, permutations: int = 32) -> tuple[int, ...]:
    grams = ngrams(text)
    return tuple(
        min((int(hashlib.sha256((str(i) + g).encode()).hexdigest(), 16) for g in grams), default=0)
        for i in range(permutations)
    )

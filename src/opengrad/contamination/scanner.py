import hashlib
import re
from collections.abc import Iterable


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().casefold()


def exact_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()


def exact_overlap(left: Iterable[str], right: Iterable[str]) -> set[str]:
    rhs = {exact_hash(x) for x in right}
    return {exact_hash(x) for x in left if exact_hash(x) in rhs}

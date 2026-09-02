from opengrad.contamination.scanner import exact_hash, exact_overlap


def test_normalized_exact_overlap():
    assert exact_hash("A  B") == exact_hash(" a b ")
    assert len(exact_overlap(["A  B", "unique"], ["a b"])) == 1

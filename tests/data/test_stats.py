from opengrad.data.mixture import analyze
from opengrad.data.stats import stats


def test_stats_and_mixture_distinguish_sample_and_token_shares():
    records = [
        {"source": "a", "messages": [], "token_count": 90},
        {"source": "b", "messages": [], "token_count": 10},
    ]
    assert stats(records)["samples"] == 2
    result = analyze(records)
    assert (
        result["sample_share"]["a"] == result["sample_share"]["b"]
        and result["token_share"]["a"] == 0.9
    )

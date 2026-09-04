import pytest

from opengrad.data.adapters import adapt_when2call_evaluation, adapt_when2call_preference
from opengrad.data.canonical import CanonicalPreferenceExample
from opengrad.data.selection import validate_training_records


def test_preference_adapter_preserves_chosen_and_rejected_separately():
    result = adapt_when2call_preference(
        {
            "uuid": "p1",
            "tools": [],
            "messages": [{"role": "user", "content": "details"}],
            "chosen_response": {"role": "assistant", "content": "Which domain?"},
            "rejected_response": {"role": "assistant", "content": "Call with invented domain"},
        }
    )
    result.validate()
    assert result.metadata["eligibility"] == "preference_only"
    assert result.chosen != result.rejected


def test_preference_rejects_identical_candidates():
    result = CanonicalPreferenceExample(
        "p1",
        {},
        [],
        [],
        {"role": "assistant", "content": "same"},
        {"role": "assistant", "content": "same"},
    )
    with pytest.raises(ValueError, match="must differ"):
        result.validate()


def test_evaluation_is_explicitly_evaluation_only():
    result = adapt_when2call_evaluation(
        {"uuid": "e1", "question": "q", "correct_answer": "direct", "answers": {}, "tools": []}
    )
    result.validate()
    assert result.metadata["eligibility"] == "evaluation_only"


def test_clean_training_rejects_evaluation_and_contaminated_rows():
    with pytest.raises(ValueError, match="forbidden"):
        validate_training_records(
            [
                {"id": "eval", "metadata": {"eligibility": "evaluation_only"}},
                {"id": "tau", "metadata": {"contamination_status": "CONTAMINATED"}},
            ]
        )

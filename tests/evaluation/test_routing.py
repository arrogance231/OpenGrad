from opengrad.evaluation.routing import routing_metrics


def test_routing_metrics_expose_directional_confusion():
    result = routing_metrics(
        ["CALL", "CALL", "ANSWER", "CLARIFY", "UNSUPPORTED"],
        ["CALL", "ANSWER", "CALL", "CLARIFY", "UNSUPPORTED"],
    )
    assert result["confusion_matrix"]["CALL"]["ANSWER"] == 1
    assert result["under_call_rate"] == 0.5
    assert result["over_call_rate"] == 1 / 3
    assert 0 < result["call_f1"] < 1

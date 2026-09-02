from opengrad.data.canonical import ToolConversation


def test_canonical_fixture_validates():
    c = ToolConversation(
        "fixture-1", "synthetic", [], [{"role": "user", "content": "hi"}], {"split": "development"}
    )
    c.validate()


def test_split_is_required():
    c = ToolConversation("fixture-1", "synthetic", [], [], {})
    try:
        c.validate()
    except ValueError:
        pass
    else:
        assert False

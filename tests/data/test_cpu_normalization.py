from opengrad.data.renderers import Qwen35_2BRenderer


def test_renderer_is_lazy_and_does_not_initialize_model_or_cuda():
    renderer = Qwen35_2BRenderer()
    assert renderer._tokenizer is None
    assert renderer.model_revision == "15852e8c16360a2fea060d615a32b45270f8a8fc"

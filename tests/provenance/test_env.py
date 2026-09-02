from pathlib import Path

from opengrad.env_capture import capture, write_capture


def test_environment_capture_is_gpu_safe_and_serializable(tmp_path: Path):
    result = capture(Path(__file__).parents[2])
    assert result["python"] and result["gpu_probe"] == "not performed by Phase 0.5"
    assert write_capture(Path(__file__).parents[2], tmp_path / "env.json").exists()

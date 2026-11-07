import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("repo_main", ROOT / "main.py")
assert SPEC is not None
assert SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_build_welcome_message() -> None:
    assert module.build_welcome_message() == "Hello from mcp-starter-kit!"

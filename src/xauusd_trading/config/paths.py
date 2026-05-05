from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_ROOT = PROJECT_ROOT / "src"
RESEARCH_ROOT = PROJECT_ROOT / "research"
DOCS_ROOT = PROJECT_ROOT / "docs"
WORKSPACE_ROOT = PROJECT_ROOT.parents[2]
DATA_ROOT = WORKSPACE_ROOT / "data" / "xauusd"


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)

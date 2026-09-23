def get_fixtures_path() -> Path:
    pytorch_dir = Path(__file__).resolve().parents[3]
    fixtures_path = pytorch_dir / "test" / "jit" / "fixtures"
    return fixtures_path

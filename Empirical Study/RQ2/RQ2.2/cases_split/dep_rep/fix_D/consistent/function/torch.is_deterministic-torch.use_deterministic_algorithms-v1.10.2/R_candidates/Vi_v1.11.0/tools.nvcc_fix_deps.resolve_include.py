def resolve_include(path: Path, include_dirs: List[Path]) -> Path:
    for include_path in include_dirs:
        abs_path = include_path / path
        if abs_path.exists():
            return abs_path

    paths = "\n    ".join(str(d / path) for d in include_dirs)
    raise RuntimeError(
        f"""
ERROR: Failed to resolve dependency:
    {path}
Tried the following paths, but none existed:
    {paths}
"""
    )

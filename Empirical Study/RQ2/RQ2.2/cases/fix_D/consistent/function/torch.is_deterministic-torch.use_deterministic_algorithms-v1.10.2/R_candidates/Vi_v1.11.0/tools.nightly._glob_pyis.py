def _glob_pyis(d: str) -> Set[str]:
    search = os.path.join(d, "**", "*.pyi")
    pyis = {os.path.relpath(p, d) for p in glob.iglob(search)}
    return pyis

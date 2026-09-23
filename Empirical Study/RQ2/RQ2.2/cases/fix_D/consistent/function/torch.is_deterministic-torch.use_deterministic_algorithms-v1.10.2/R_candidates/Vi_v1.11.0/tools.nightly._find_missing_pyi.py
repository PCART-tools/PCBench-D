def _find_missing_pyi(source_dir: str, target_dir: str) -> List[str]:
    source_pyis = _glob_pyis(source_dir)
    target_pyis = _glob_pyis(target_dir)
    missing_pyis = [os.path.join(source_dir, p) for p in (source_pyis - target_pyis)]
    missing_pyis.sort()
    return missing_pyis

def _exec_with_source(src: str, globals: Dict[str, Any]):
    key = _loader.cache(src, globals)
    exec(compile(src, key, 'exec'), globals)

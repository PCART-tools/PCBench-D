def _flexhash(elem: Any) -> int:
    """Hashing that also handles lists/dicts (for 'unique' check)."""
    if isinstance(elem, list):
        return hash(tuple(_flexhash(e) for e in elem))
    elif isinstance(elem, dict):
        return hash((_flexhash(k), _flexhash(v)) for k, v in elem.items())
    return hash(elem)

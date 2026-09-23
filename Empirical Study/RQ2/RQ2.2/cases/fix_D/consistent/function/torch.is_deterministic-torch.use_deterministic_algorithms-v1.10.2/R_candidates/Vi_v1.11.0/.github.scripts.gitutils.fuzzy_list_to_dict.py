def fuzzy_list_to_dict(items: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    Converts list to dict preserving elements with duplicate keys
    """
    rc: Dict[str, List[str]] = defaultdict(lambda: [])
    for (key, val) in items:
        rc[key].append(val)
    return dict(rc)

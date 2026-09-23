def from_includes(includes: List[Dict[str, str]]) -> str:
    return json.dumps({"include": includes})

def _get_node_base_name(node_name: str) -> tuple[str, int | None]:
    pattern = r"(.*)\.(\d+)"
    match = re.match(pattern, node_name)
    if match is not None:
        base_name, count_str = match.groups()
        return base_name, int(count_str)
    return node_name, None

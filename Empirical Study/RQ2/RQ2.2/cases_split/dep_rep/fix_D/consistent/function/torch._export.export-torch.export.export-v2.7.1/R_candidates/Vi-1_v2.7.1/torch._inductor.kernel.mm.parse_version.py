def parse_version(version_string: str) -> Optional[tuple[int, ...]]:
    pattern = r"(\d+)\.(\d+)?"
    match = re.match(pattern, version_string)

    if match:
        return tuple(int(group) for group in match.groups())
    else:
        return None

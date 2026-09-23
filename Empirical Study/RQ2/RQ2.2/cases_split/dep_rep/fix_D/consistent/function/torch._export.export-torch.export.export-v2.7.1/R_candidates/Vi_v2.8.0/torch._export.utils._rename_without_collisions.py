def _rename_without_collisions(
    name_map: dict[str, str],
    orig_name: str,
    name: str,
    is_placeholder: bool = False,
):
    """
    Renames nodes to avoid name collisions, with suffixing.
    name_map: map from original name to new name
    orig_name: mapping key
    name: candidate name (potentially suffixed, e.g. mul_2)
    is_placeholder: if the node is a placeholder, avoid detecting suffix
    """
    if name in name_map.values():
        # non-placeholder nodes may be suffixed with the count
        # instead of adding another suffix, we will try to increment it
        match = re.match(r"(.*)_(\d+)", name)
        if match and not is_placeholder:
            name, n = match.group(1), int(match.group(2))
        else:
            n = 0
        while (dup_name := f"{name}_{n + 1}") in name_map.values():
            n += 1
        name_map[orig_name] = dup_name
    else:
        name_map[orig_name] = name
    return name_map[orig_name]

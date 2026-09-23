def key_path_to_source(kp: KeyPath) -> Source:
    """
    Given a key path, return the source for the key path.
    """
    source: Source = LocalSource("args")
    for k in kp:
        if isinstance(k, SequenceKey):
            source = GetItemSource(source, k.idx)
        elif isinstance(k, MappingKey):
            source = GetItemSource(source, k.key)
        elif isinstance(k, GetAttrKey):
            source = AttrSource(source, k.name)
        else:
            raise ValueError(f"Unknown KeyEntry {k}")

    return source

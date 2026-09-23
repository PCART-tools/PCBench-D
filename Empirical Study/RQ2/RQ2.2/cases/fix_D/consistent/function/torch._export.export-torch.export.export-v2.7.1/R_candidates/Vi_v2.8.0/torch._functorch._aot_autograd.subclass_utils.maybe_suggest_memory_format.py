def maybe_suggest_memory_format(
    t, with_memory_format: bool
) -> Optional[MemoryFormatMeta]:
    if not with_memory_format:
        return None

    return MemoryFormatMeta.from_tensor(t)

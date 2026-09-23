def may_convert_to_optional(
    value: Optional[Sequence[_T]],
) -> Optional[Sequence[Optional[_T]]]:
    if isinstance(value, list) and not value:
        # [None] makes sure the cpp wrapper codegen will generate something like
        # {std::nullopt} instead of {}
        return [None]
    return value

def returns_type(rs: Sequence[Return]) -> CType:
    # At present, there is no difference. But there could be!
    return cpp.returns_type(rs)

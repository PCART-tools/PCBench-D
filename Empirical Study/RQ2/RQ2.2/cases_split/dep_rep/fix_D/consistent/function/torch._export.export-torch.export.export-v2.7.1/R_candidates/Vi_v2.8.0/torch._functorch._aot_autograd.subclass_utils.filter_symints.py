def filter_symints(lst: Iterable[IntLikeType]):
    # Capture all SymInts from the iterable.
    def symint_check(s: IntLikeType) -> bool:
        return isinstance(s, SymInt) and not s.node.is_nested_int()

    return [s for s in lst if symint_check(s)]

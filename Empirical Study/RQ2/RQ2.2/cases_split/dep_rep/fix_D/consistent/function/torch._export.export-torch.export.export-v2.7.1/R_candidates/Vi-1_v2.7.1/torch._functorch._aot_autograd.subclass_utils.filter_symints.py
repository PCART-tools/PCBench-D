def filter_symints(lst: Iterable[Union[int, SymInt]]):
    # Capture all SymInts from the iterable.
    def symint_check(s: Union[int, SymInt]) -> bool:
        return isinstance(s, SymInt) and not s.node.is_nested_int()

    return [s for s in lst if symint_check(s)]

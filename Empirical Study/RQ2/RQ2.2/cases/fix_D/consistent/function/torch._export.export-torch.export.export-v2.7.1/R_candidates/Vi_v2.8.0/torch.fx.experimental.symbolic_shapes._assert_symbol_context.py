def _assert_symbol_context(symbolic_context: object) -> TypeGuard[SymbolicContext]:
    assert isinstance(symbolic_context, SymbolicContext), (
        "Invalid symbolic_context object"
    )
    assert type(symbolic_context) is not SymbolicContext, (
        "Illegal usage of symbolic_context ABC"
    )
    return True

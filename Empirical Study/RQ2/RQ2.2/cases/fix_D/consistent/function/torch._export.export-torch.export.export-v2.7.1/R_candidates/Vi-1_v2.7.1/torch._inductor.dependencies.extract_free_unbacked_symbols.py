def extract_free_unbacked_symbols(
    fn: Callable[..., Any],
    index: Sequence[sympy.Expr],
    rindex: Optional[Sequence[sympy.Expr]] = None,
) -> OrderedSet[sympy.Symbol]:
    from .ir import FlexibleLayout

    args = [index, rindex] if rindex is not None else [index]
    handler = FreeUnbackedSymbolsOpsHandler()
    # NB: I cargo culted the allow_indexing patch here, I don't understand why
    # people do this all over
    with (
        V.set_ops_handler(handler),
        patch.object(FlexibleLayout, "allow_indexing", True),
    ):
        fn(*args)
    return handler.symbols

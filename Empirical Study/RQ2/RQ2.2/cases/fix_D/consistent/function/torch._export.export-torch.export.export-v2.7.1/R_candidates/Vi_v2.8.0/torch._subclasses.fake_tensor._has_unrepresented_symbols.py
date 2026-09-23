def _has_unrepresented_symbols(
    state: _CacheKeyState, output: Optional[FakeTensor]
) -> bool:
    from torch.fx.experimental.symbolic_shapes import _iterate_exprs

    for s in _iterate_exprs(output):
        for symbol in s.free_symbols:
            if symbol not in state.known_symbols:
                return True

    return False

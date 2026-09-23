def resolve_unbacked_bindings(
    shape_env: Optional[ShapeEnv],
    bindings: Optional[dict[sympy.Symbol, pytree.KeyPath]],
) -> Optional[dict[sympy.Symbol, pytree.KeyPath]]:
    if bindings is None:
        return None
    assert shape_env is not None
    return {shape_env.unbacked_renamings.get(k, k): v for k, v in bindings.items()}

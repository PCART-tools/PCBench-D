def bind_symbols(gm: torch.fx.GraphModule, *args: Tensor) -> dict[sympy.Symbol, int]:
    return gm.shape_env.bind_symbols(fx_placeholder_vals(gm), args)  # type: ignore[operator, union-attr]

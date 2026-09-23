def eval_guards(
    gm: torch.fx.GraphModule, *args: Tensor, ignore_static: bool = True
) -> bool:
    return gm.shape_env.evaluate_guards_for_args(  # type: ignore[operator, union-attr]
        fx_placeholder_vals(gm), args, ignore_static=ignore_static
    )

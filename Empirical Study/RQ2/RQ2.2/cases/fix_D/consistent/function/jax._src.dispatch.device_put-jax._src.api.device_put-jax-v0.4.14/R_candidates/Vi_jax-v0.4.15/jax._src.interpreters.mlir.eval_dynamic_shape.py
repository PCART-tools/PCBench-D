def eval_dynamic_shape(ctx: LoweringRuleContext,
                       shape: core.Shape) -> tuple[int | Value, ...]:
  if config.jax_dynamic_shapes:
    return tuple(ctx.axis_size_env.get(d, d) for d in shape)  # type: ignore
  else:
    ctx = ctx.replace(
        primitive="eval_dynamic_shape",
        avals_in=[core.dim_value_aval()] * len(ctx.module_context.shape_poly_state.dim_vars))

    res = lower_fun(
        partial(core.evaluate_shape, shape, ctx.module_context.shape_poly_state.dim_vars),
        multiple_results=True)(ctx, *ctx.dim_var_values)
    return tuple(operator.index(d) if core.is_constant_dim(d) else d_ir
                 for d, d_ir in zip(shape, util.flatten(res)))  # type: ignore

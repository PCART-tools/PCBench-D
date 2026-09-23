def eval_dynamic_shape(ctx: LoweringRuleContext,
                       shape: core.Shape) -> Tuple[Union[int, Value], ...]:
  # assert not core.is_constant_shape(shape)
  if config.jax_dynamic_shapes:
    return tuple(ctx.axis_size_env.get(d, d) for d in shape)  # type: ignore
  else:
    dim_var_env = {dv_name : DimExprEvaluator(dv_val[0])
                   for dv_name, dv_val in zip(ctx.module_context.dim_vars, ctx.dim_var_values)}
    def eval_dim(d: core.DimSize) -> Union[int, ir.Value]:
      try:
        return operator.index(d)
      except:
        if isinstance(d, ir.Value):
          return d
        else:
          # Is a dimension polynomial
          return d.evaluate(dim_var_env).value  # type: ignore
    return tuple(eval_dim(d) for d in shape)

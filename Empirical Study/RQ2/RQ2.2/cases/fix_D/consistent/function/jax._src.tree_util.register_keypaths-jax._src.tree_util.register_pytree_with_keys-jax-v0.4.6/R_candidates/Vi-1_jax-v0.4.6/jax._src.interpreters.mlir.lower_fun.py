def lower_fun(fun: Callable, multiple_results: bool = True) -> Callable:
  """Converts a traceable JAX function `fun` into a lowering rule.

  The returned function does not use `avals_out`, so callers may pass any value
  as `avals_out`."""
  def f_lowered(ctx, *args, **params):
    f = fun if multiple_results else lambda *args, **kw: (fun(*args, **kw),)
    wrapped_fun = lu.wrap_init(f, params)

    if config.jax_dynamic_shapes:
      # We might be applying this function to arguments with dynamic shapes,
      # i.e. there might be Vars in the shape tuples of ctx.avals_in. In that
      # case, we need to form a jaxpr with leading binders for those axis size
      # arguments (by computing an InputType and using trace_to_jaxpr_dynamic2),
      # and we need to call jaxpr_subcomp with these arguments made explicit.
      args = (*ctx.axis_size_env.values(), *args)
      idx = {d: core.DBIdx(i) for i, d in enumerate(ctx.axis_size_env)}
      i32_aval = core.ShapedArray((), np.dtype('int32'))
      implicit_args = [(i32_aval, False)] * len(ctx.axis_size_env)
      explicit_args = [(a.update(shape=tuple(idx.get(d, d) for d in a.shape))
                        if type(a) is core.DShapedArray else a, True)
                       for a in ctx.avals_in]
      wrapped_fun = lu.annotate(wrapped_fun, (*implicit_args, *explicit_args))
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic2(wrapped_fun)
    else:
      jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, ctx.avals_in)
      # TODO(frostig,mattjj): check ctx.avals_out against jaxpr avals out?

    out, tokens = jaxpr_subcomp(
        ctx.module_context, jaxpr, ctx.tokens_in, _ir_consts(consts),
        *map(wrap_singleton_ir_values, args), dim_var_values=ctx.dim_var_values)
    ctx.set_tokens_out(tokens)
    return out

  return f_lowered

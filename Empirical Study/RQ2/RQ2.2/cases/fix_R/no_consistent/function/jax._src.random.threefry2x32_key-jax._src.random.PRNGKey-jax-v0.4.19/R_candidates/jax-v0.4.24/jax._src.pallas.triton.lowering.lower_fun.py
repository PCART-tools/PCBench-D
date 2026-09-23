def lower_fun(
    fun: Callable[..., Any], *, multiple_results: bool
) -> Callable[..., Any]:
  fn = fun if multiple_results else lambda *args, **kw: (fun(*args, **kw),)

  def f_lowered(ctx: TritonLoweringRuleContext, *args, **params):
    wrapped_fun = lu.wrap_init(fn, params)
    jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(wrapped_fun, ctx.avals_in)
    jaxpr = jax_core.ClosedJaxpr(jaxpr, consts)
    out = _closed_call_lowering_rule(ctx, *args, call_jaxpr=jaxpr)
    return out if multiple_results else out[0]

  return f_lowered

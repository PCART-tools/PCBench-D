def core_call_lowering(ctx: LoweringRuleContext,
                       *args, name, backend=None, call_jaxpr):
  out_nodes, tokens = _call_lowering(
      name, name, call_jaxpr, backend, ctx.module_context,
      ctx.avals_in, ctx.avals_out, ctx.tokens_in, *args,
      dim_var_values=ctx.dim_var_values)
  ctx.set_tokens_out(tokens)
  return out_nodes

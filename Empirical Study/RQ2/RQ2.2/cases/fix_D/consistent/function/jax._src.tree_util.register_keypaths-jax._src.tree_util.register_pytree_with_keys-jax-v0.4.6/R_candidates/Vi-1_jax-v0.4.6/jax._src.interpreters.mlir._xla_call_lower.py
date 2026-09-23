def _xla_call_lower(ctx, *args,
                    backend=None, name, call_jaxpr, donated_invars, inline=None,
                    device=None, keep_unused=None):
  del device, donated_invars, inline, keep_unused  # Ignored.
  out_nodes, tokens = _call_lowering(
      name, util.wrap_name(name, "jit"), call_jaxpr, backend,
      ctx.module_context, ctx.avals_in, ctx.avals_out, ctx.tokens_in,
      *args, dim_var_values=ctx.dim_var_values)
  ctx.set_tokens_out(tokens)
  return out_nodes

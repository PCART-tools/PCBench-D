def _custom_jvp_call_mlir_translation(ctx, *args, call_jaxpr, jvp_jaxpr_thunk,
                                      num_consts, symbolic_zeros):
  del jvp_jaxpr_thunk, num_consts, symbolic_zeros
  args_ = map(mlir.wrap_singleton_ir_values, args)
  consts = mlir._ir_consts(call_jaxpr.consts)
  out, tokens = mlir.jaxpr_subcomp(ctx.module_context, call_jaxpr.jaxpr,
                                   ctx.tokens_in, consts, *args_,
                                   dim_var_values=ctx.dim_var_values)
  ctx.set_tokens_out(tokens)
  return out

def _pjit_lowering(ctx, *args, name, jaxpr, in_shardings,
                   out_shardings, resource_env, donated_invars,
                   keep_unused, inline):
  effects = list(ctx.tokens_in.effects())
  output_types = map(mlir.aval_to_ir_types, ctx.avals_out)
  output_types = [mlir.token_type()] * len(effects) + output_types
  flat_output_types = util.flatten(output_types)

  arg_shardings = [None if _is_unspecified(i) else i._to_xla_op_sharding(aval.ndim)
                   for aval, i in zip(ctx.avals_in, in_shardings)]
  result_shardings = [None if _is_unspecified(o) else o._to_xla_op_sharding(aval.ndim)
                      for aval, o in zip(ctx.avals_out, out_shardings)]

  # TODO(b/228598865): inlined calls cannot have shardings set directly on the
  # inputs or outputs because they are lost during MLIR->HLO conversion.
  # using_sharding_annotation=False means we add an identity operation instead.
  func = mlir.lower_jaxpr_to_fun(
      ctx.module_context, name, jaxpr, effects, arg_shardings=arg_shardings,
      result_shardings=result_shardings, use_sharding_annotations=False,
      api_name=('jit' if resource_env is None else 'pjit'))
  tokens_in = [ctx.tokens_in.get(eff) for eff in effects]
  args = (*ctx.dim_var_values, *tokens_in, *args)
  call = func_dialect.CallOp(flat_output_types,
                             ir.FlatSymbolRefAttr.get(func.name.value),
                             mlir.flatten_lowering_ir_args(args))
  out_nodes = util.unflatten(call.results, map(len, output_types))
  tokens, out_nodes = split_list(out_nodes, [len(effects)])
  tokens_out = ctx.tokens_in.update_tokens(mlir.TokenSet(zip(effects, tokens)))
  ctx.set_tokens_out(tokens_out)
  return out_nodes

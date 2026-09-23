def _call_lowering(fn_name, stack_name, call_jaxpr, backend, ctx, avals_in,
                   avals_out, tokens_in, *args,
                   dim_var_values: Sequence[ir.Value],
                   arg_names=None, result_names=None):
  if isinstance(call_jaxpr, core.Jaxpr):
    call_jaxpr = core.ClosedJaxpr(call_jaxpr, ())
  xla.check_backend_matches(backend, ctx.platform)
  effects = list(tokens_in.effects())
  output_types = map(aval_to_ir_types, avals_out)
  output_types = [token_type()] * len(effects) + output_types
  flat_output_types = util.flatten(output_types)
  symbol_name = _lower_jaxpr_to_fun_cached(
      ctx, fn_name, call_jaxpr, effects, arg_names=arg_names,
      result_names=result_names).name.value
  tokens = [tokens_in.get(eff) for eff in effects]
  args = tuple([*dim_var_values, *tokens, *args])
  call = func_dialect.CallOp(flat_output_types,
                             ir.FlatSymbolRefAttr.get(symbol_name),
                             flatten_lowering_ir_args(args))
  out_nodes = util.unflatten(call.results, map(len, output_types))
  tokens, out_nodes = util.split_list(out_nodes, [len(effects)])
  tokens_out = tokens_in.update_tokens(TokenSet(zip(effects, tokens)))
  return out_nodes, tokens_out

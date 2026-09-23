def _emit_lowering_rule_as_fun(lowering_rule,
                               ctx: LoweringRuleContext) -> func_dialect.FuncOp:
  """Emits the contents of a lowering rule as a private function."""
  num_dim_vars = len(ctx.module_context.dim_vars)
  # TODO(necula) maybe only pass the dim_vars if they are needed?
  dim_var_types = map(aval_to_ir_types, [core.ShapedArray((), dtypes.canonicalize_dtype(np.int64))] * num_dim_vars)

  input_types = map(aval_to_ir_types, ctx.avals_in)
  output_types = map(aval_to_ir_types, ctx.avals_out)
  effs = list(ctx.tokens_in.effects())
  token_types = [token_type() for _ in effs]
  input_types = [*dim_var_types, *token_types, *input_types]
  output_types = [*token_types, *output_types]

  flat_input_types = util.flatten(input_types)
  flat_output_types = util.flatten(output_types)
  ftype = ir.FunctionType.get(flat_input_types, flat_output_types)
  assert ctx.primitive is not None
  func_op = func_dialect.FuncOp(ctx.primitive.name, ftype,
                                ip=ctx.module_context.ip)
  func_op.attributes["sym_visibility"] = ir.StringAttr.get("private")
  ctx.module_context.symbol_table.insert(func_op)
  entry_block = func_op.add_entry_block()
  with ir.InsertionPoint(entry_block):
    unflattened_args = util.unflatten(entry_block.arguments,
                                      map(len, input_types))
    dim_var_values, token_args, unflattened_args = util.split_list(unflattened_args, [num_dim_vars, len(ctx.tokens_in)])
    sub_ctx = ctx.replace(tokens_in=TokenSet(zip(effs, token_args)),
                          dim_var_values=dim_var_values)
    outs = lowering_rule(sub_ctx, *_unwrap_singleton_ir_values(unflattened_args))
    if sub_ctx.tokens_out:
      outs = [*[sub_ctx.tokens_out.get(eff) for eff in effs], outs]
    func_dialect.ReturnOp(util.flatten(map(wrap_singleton_ir_values, outs)))
  return func_op

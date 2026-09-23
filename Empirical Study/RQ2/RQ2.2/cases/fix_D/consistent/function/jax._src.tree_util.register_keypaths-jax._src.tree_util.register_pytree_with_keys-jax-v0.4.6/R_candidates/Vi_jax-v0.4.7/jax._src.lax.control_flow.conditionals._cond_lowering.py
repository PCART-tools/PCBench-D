def _cond_lowering(ctx, index, *args, branches, linear):
  del linear  # Unused.
  joined_effects = core.join_effects(*(branch.effects for branch in branches))
  ordered_effects = list(effects.ordered_effects.filter_in(joined_effects))
  num_tokens = len(ordered_effects)
  tokens_in = ctx.tokens_in.subset(ordered_effects)
  output_token_types = [mlir.token_type() for _ in ordered_effects]
  output_types = [
      *output_token_types, *map(mlir.aval_to_ir_types, ctx.avals_out)]
  flat_output_types = util.flatten(output_types)

  # CaseOp takes a single argument 'index' and the corresponding blocks
  # have no arguments; the computation within the block uses implicit
  # captures.
  case_op = hlo.CaseOp(flat_output_types, index=index,
                       num_branches=len(branches))
  name_stack = ctx.module_context.name_stack.extend('cond')
  for i, jaxpr in enumerate(branches):
    branch = case_op.regions[i].blocks.append()
    with ir.InsertionPoint(branch):
      sub_ctx = ctx.module_context.replace(
          name_stack=name_stack.extend(f'branch_{i}_fun'))
      out_vals, tokens_out = mlir.jaxpr_subcomp(
          sub_ctx, jaxpr.jaxpr, tokens_in,
          map(mlir.ir_constants, jaxpr.consts),
          *map(mlir.wrap_singleton_ir_values, args),
          dim_var_values=ctx.dim_var_values)
      out_tokens = [tokens_out.get(eff) for eff in ordered_effects]
      out_vals = [*out_tokens, *out_vals]
      hlo.ReturnOp(util.flatten(out_vals))

  tokens_and_outputs = util.unflatten(case_op.results, map(len, output_types))
  tokens, outputs = util.split_list(tokens_and_outputs, [num_tokens])
  ctx.set_tokens_out(mlir.TokenSet(zip(ordered_effects, tokens)))
  return outputs

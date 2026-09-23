def _while_lowering(ctx, *args, cond_jaxpr, body_jaxpr, cond_nconsts,
                    body_nconsts):
  pred_aval = cond_jaxpr.out_avals[0]
  batched = bool(pred_aval.shape)
  cond_ordered_effects = effects.ordered_effects.filter_in(cond_jaxpr.effects)
  if cond_ordered_effects:
    def cond(args):
      # Pred can be batched
      pred = core.eval_jaxpr(cond_jaxpr.jaxpr, cond_jaxpr.consts, *args)[0]
      if batched:
        pred = lax._reduce_or(pred, tuple(range(len(pred_aval.shape))))
      return pred
    def body(args):
      return tuple(core.eval_jaxpr(body_jaxpr.jaxpr, body_jaxpr.consts, *args))
    def new_cond(pred_args):
      pred, _ = pred_args
      return pred
    def new_body(pred_args):
      _, args  = pred_args
      args = body(args)
      pred = cond(args)
      return pred, args
    def fun(*args):
      pred = cond(args)
      _, out = while_loop(new_cond, new_body, (pred, args))
      return out
    return mlir.lower_fun(fun)(ctx, *args)

  loop_carry_types = _map(mlir.aval_to_ir_types, ctx.avals_in)
  body_effects = effects.ordered_effects.filter_in(body_jaxpr.effects)
  num_tokens = len(body_effects)
  tokens = [ctx.tokens_in.get(eff) for eff in body_effects]
  token_types = [mlir.token_type() for _ in tokens]
  loop_carry_types = [*token_types, *loop_carry_types]
  flat_loop_carry_types = util.flatten(loop_carry_types)
  args = [*tokens, *args]

  flat_args = mlir.flatten_lowering_ir_args(args)
  while_op = hlo.WhileOp(flat_loop_carry_types, flat_args)

  # Loop condition
  cond_block = while_op.regions[0].blocks.append(*flat_loop_carry_types)
  name_stack = ctx.module_context.name_stack.extend('while')
  with ir.InsertionPoint(cond_block):
    flat_cond_args = [
        cond_block.arguments[i] for i in range(len(flat_loop_carry_types))
    ]
    cond_args = util.unflatten(flat_cond_args, _map(len, loop_carry_types))
    # Remove tokens from cond args
    cond_args = cond_args[num_tokens:]
    x, _, z = util.split_list(cond_args, [cond_nconsts, body_nconsts])
    cond_ctx = ctx.module_context.replace(name_stack=name_stack.extend('cond'))
    ((pred,),), _ = mlir.jaxpr_subcomp(cond_ctx, cond_jaxpr.jaxpr, mlir.TokenSet(),
                                       _map(mlir.ir_constants, cond_jaxpr.consts),
                                       *(x + z), dim_var_values=ctx.dim_var_values)
    if batched:
      pred_ctx = mlir.LoweringRuleContext(
          module_context=ctx.module_context,
          primitive=None,
          avals_in=[pred_aval],
          avals_out=[pred_aval.update(shape=())],
          tokens_in=mlir.TokenSet(),
          tokens_out=None)
      pred, = lax._unary_reduce_lower(
          hlo.OrOp,
          lambda dtype: np.array(False, dtype),
          pred_ctx,
          pred,
          axes=tuple(range(len(pred_aval.shape))))
    hlo.ReturnOp([pred])

  # Loop body
  body_block = while_op.regions[1].blocks.append(*flat_loop_carry_types)
  with ir.InsertionPoint(body_block):
    flat_body_args = [
        body_block.arguments[i] for i in range(len(flat_loop_carry_types))
    ]
    body_args = util.unflatten(flat_body_args, _map(len, loop_carry_types))
    # Tokens are at the front of the args list to the while loop
    token_args, body_args = util.split_list(body_args, [num_tokens])
    tokens_in = mlir.TokenSet(zip(body_effects, token_args))
    x, y, z = util.split_list(body_args, [cond_nconsts, body_nconsts])
    body_ctx = ctx.module_context.replace(name_stack=name_stack.extend('body'))
    new_z, tokens_out = mlir.jaxpr_subcomp(body_ctx, body_jaxpr.jaxpr,
        tokens_in, _map(mlir.ir_constants, body_jaxpr.consts),
        *(y + z), dim_var_values=ctx.dim_var_values)
    out_tokens = [tokens_out.get(eff) for eff in body_effects]
    if batched:
      body_pred_ctx = ctx.module_context.replace(
          name_stack=name_stack.extend('body_pred'))
      ((body_pred,),), _ = mlir.jaxpr_subcomp(
          body_pred_ctx, cond_jaxpr.jaxpr, mlir.TokenSet(),
          _map(mlir.ir_constants, cond_jaxpr.consts),
          *(x + z), dim_var_values=ctx.dim_var_values)
      new_z = _map(
          partial(_pred_bcast_select_hlo, ctx, pred_aval, body_pred), new_z, z,
          body_jaxpr.out_avals)

    hlo.ReturnOp([*util.flatten(out_tokens), *util.flatten(x),
                  *util.flatten(y), *util.flatten(new_z)])

  outputs = util.unflatten(while_op.results, _map(len, loop_carry_types))
  tokens, _, _, z = util.split_list(outputs, [num_tokens, cond_nconsts, body_nconsts])
  if tokens:
    ctx.set_tokens_out(mlir.TokenSet(zip(body_effects, tokens)))
  return z

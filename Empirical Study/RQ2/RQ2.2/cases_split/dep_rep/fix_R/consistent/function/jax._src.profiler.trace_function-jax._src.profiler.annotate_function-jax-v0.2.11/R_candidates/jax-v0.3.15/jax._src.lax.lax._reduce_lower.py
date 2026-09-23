def _reduce_lower(ctx, *values, computation, jaxpr, consts, dimensions):
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in), ctx.avals_in
  operands, init_values = util.split_list(values, [len(values) // 2])
  init_value_avals = ctx.avals_in[len(values) // 2:]
  op = mhlo.ReduceOp([mlir.aval_to_ir_type(aval) for aval in ctx.avals_out],
                     operands, init_values, mlir.dense_int_elements(dimensions))
  ir_types = [mlir.aval_to_ir_type(aval) for aval in init_value_avals]
  reducer = op.regions[0].blocks.append(*(ir_types + ir_types))
  with ir.InsertionPoint(reducer):
    reducer_ctx = ctx.module_context.replace(name_stack=util.new_name_stack())
    if jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `reduce`.')
    out_nodes, _ = mlir.jaxpr_subcomp(reducer_ctx, jaxpr, mlir.TokenSet(), consts,
                                      *([a] for a in reducer.arguments))
    mhlo.ReturnOp(util.flatten(out_nodes))
  return op.results

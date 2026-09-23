def _sort_lower(ctx, *operands, dimension, is_stable, num_keys):
  assert all(isinstance(x, core.ShapedArray) for x in ctx.avals_in), ctx.avals_in
  sort = mhlo.SortOp([mlir.aval_to_ir_type(aval) for aval in ctx.avals_out],
                     mlir.flatten_lowering_ir_args(operands),
                     dimension=mlir.i64_attr(dimension),
                     is_stable=ir.BoolAttr.get(is_stable))
  scalar_avals = [aval.update(shape=()) for aval in ctx.avals_in]
  scalar_types = safe_map(mlir.aval_to_ir_type, scalar_avals)
  comparator = sort.comparator.blocks.append(
      *util.flatten(zip(scalar_types, scalar_types)))
  with ir.InsertionPoint(comparator):
    lower_comparator = mlir.lower_fun(partial(_sort_lt_comparator),
                                      multiple_results=False)
    sub_ctx = ctx.replace(primitive=None,
                          avals_in=util.flatten(zip(scalar_avals, scalar_avals)),
                          avals_out=[core.ShapedArray((), np.bool_)])

    out = lower_comparator(sub_ctx, *[[a] for a in comparator.arguments],
                           num_keys=num_keys)
    mhlo.ReturnOp(util.flatten(out))
  return sort.results

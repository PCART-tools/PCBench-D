def _scatter_lower(ctx, operand, indices, updates, *,
                   update_jaxpr, update_consts, dimension_numbers,
                   indices_are_sorted, unique_indices, mode):
  if mode == GatherScatterMode.CLIP:
    clip_fn = mlir.lower_fun(_clamp_scatter_indices, multiple_results=False)
    (indices,), = clip_fn(ctx.replace(avals_out=None), operand, indices,
                          updates, dnums=dimension_numbers)

  aval_out, = ctx.avals_out
  dnums = dimension_numbers
  scatter_dnums = mhlo.ScatterDimensionNumbers.get(
    update_window_dims=list(dnums.update_window_dims),
    inserted_window_dims=list(dnums.inserted_window_dims),
    scattered_dims_to_operand_dims=list(dnums.scatter_dims_to_operand_dims),
    index_vector_dim=len(ctx.avals_in[1].shape) - 1)
  result = mlir.aval_to_ir_types(aval_out)
  operand = [operand]
  updates = [updates]
  op = mhlo.ScatterOp(
      result,
      operand,
      indices,
      updates,
      scatter_dnums,
      indices_are_sorted=ir.BoolAttr.get(indices_are_sorted),
      unique_indices=ir.BoolAttr.get(unique_indices))
  scalar_type = mlir.aval_to_ir_type(core.ShapedArray((), aval_out.dtype))
  update = op.update_computation.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(update):
    update_ctx = ctx.module_context.replace(name_stack=util.new_name_stack())
    if update_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `scatter`.')
    out_nodes, _ = mlir.jaxpr_subcomp(
        update_ctx, update_jaxpr, mlir.TokenSet(), update_consts,
        (update.arguments[0],), (update.arguments[1],))
    mhlo.ReturnOp(util.flatten(out_nodes))
  return op.results

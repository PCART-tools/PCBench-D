def _scatter_add_lower_gpu(ctx, operand, indices, updates,
                           *, update_jaxpr, update_consts, dimension_numbers,
                           indices_are_sorted, unique_indices, mode):
  operand_aval_in, _, updates_aval_in = ctx.avals_in
  if operand_aval_in.dtype != np.complex128:
    return _scatter_lower(ctx, operand, indices, updates,
                          update_jaxpr=update_jaxpr,
                          update_consts=update_consts,
                          dimension_numbers=dimension_numbers,
                          indices_are_sorted=indices_are_sorted,
                          unique_indices=unique_indices, mode=mode)

  if mode == GatherScatterMode.CLIP:
    clip_fn = mlir.lower_fun(_clamp_scatter_indices, multiple_results=False)
    (indices,), = clip_fn(ctx.replace(avals_out=None), operand, indices, updates,
                          dnums=dimension_numbers)

  aval_out, = ctx.avals_out
  dnums = dimension_numbers
  scatter_dnums = mhlo.ScatterDimensionNumbers.get(
    update_window_dims=list(dnums.update_window_dims),
    inserted_window_dims=list(dnums.inserted_window_dims),
    scattered_dims_to_operand_dims=list(dnums.scatter_dims_to_operand_dims),
    index_vector_dim=len(ctx.avals_in[1].shape) - 1)
  real_dtype = _real_dtype(aval_out.dtype)
  operand_type_part = mlir.aval_to_ir_types(
      core.ShapedArray(aval_out.shape, real_dtype))

  def _scatter(operand_part, updates_part):
    operand_part = [operand_part]
    updates_part = [updates_part]

    scatter = mhlo.ScatterOp(
        operand_type_part,
        operand_part,
        indices,
        updates_part,
        scatter_dnums,
        indices_are_sorted=ir.BoolAttr.get(indices_are_sorted),
        unique_indices=ir.BoolAttr.get(unique_indices))
    scalar_type = mlir.aval_to_ir_type(core.ShapedArray((), real_dtype))
    reducer = scatter.regions[0].blocks.append(scalar_type, scalar_type)
    with ir.InsertionPoint(reducer):
      add = mhlo.AddOp(*reducer.arguments).result
      mhlo.ReturnOp([add])
    return scatter.result

  real = _scatter(mhlo.RealOp(operand).result, mhlo.RealOp(updates).result)
  imag = _scatter(mhlo.ImagOp(operand).result, mhlo.ImagOp(updates).result)
  return mhlo.ComplexOp(real, imag).results

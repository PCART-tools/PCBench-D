def _eig_cpu_lowering(ctx, operand, *, compute_left_eigenvectors,
                      compute_right_eigenvectors):
  operand_aval, = ctx.avals_in
  out_aval = ctx.avals_out[0]
  batch_dims = operand_aval.shape[:-2]
  if jaxlib_version < (0, 4, 13):
    if any(not is_constant_shape(a.shape) for a in ctx.avals_in):
      raise NotImplementedError(
          "Shape polymorphism for eig is not implemented. "
          "Try upgrading jaxlib")
    w, vl, vr, info = lapack.geev_hlo(operand_aval.dtype, operand,  # type: ignore
                                      jobvl=compute_left_eigenvectors,
                                      jobvr=compute_right_eigenvectors)
  else:
    if jaxlib_version < (0, 4, 14):
      op_shape_vals = mlir.eval_dynamic_shape_as_vals(ctx, operand_aval.shape)
    else:
      op_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
    w, vl, vr, info = lapack.geev_hlo(operand_aval.dtype, operand,
                                      input_shape_vals=op_shape_vals,
                                      jobvl=compute_left_eigenvectors,
                                      jobvr=compute_right_eigenvectors)

  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  select_w_aval = ShapedArray(batch_dims + (1,), np.dtype(np.bool_))
  w = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_w_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_w_aval,
      w, out_aval, _nan_like_hlo(ctx, out_aval), out_aval)
  output = [w]

  if compute_left_eigenvectors:
    aval = ctx.avals_out[len(output)]
    select_vl_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
    vl = _broadcasting_select_hlo(
        ctx,
        mlir.broadcast_in_dim(ctx, ok, select_vl_aval,
                              broadcast_dimensions=range(len(batch_dims))),
        select_vl_aval,
        vl, aval, _nan_like_hlo(ctx, aval), aval)
    output.append(vl)

  if compute_right_eigenvectors:
    aval = ctx.avals_out[len(output)]
    select_vr_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
    vr = _broadcasting_select_hlo(
        ctx,
        mlir.broadcast_in_dim(ctx, ok, select_vr_aval,
                              broadcast_dimensions=range(len(batch_dims))),
        select_vr_aval,
        vr, aval, _nan_like_hlo(ctx, aval), aval)
    output.append(vr)

  return output

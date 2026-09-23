def _schur_cpu_lowering(ctx, operand, *, compute_schur_vectors, sort_eig_vals,
                        select_callable):
  operand_aval, = ctx.avals_in
  batch_dims = operand_aval.shape[:-2]

  if jaxlib_version < (0, 4, 14):
    gees_result = lapack.gees_hlo(operand_aval.dtype, operand,
                                  jobvs=compute_schur_vectors,
                                  sort=sort_eig_vals,
                                  select=select_callable)  # type: ignore
  else:
    a_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, operand_aval.shape)
    gees_result = lapack.gees_hlo(operand_aval.dtype, operand,
                                  jobvs=compute_schur_vectors,
                                  sort=sort_eig_vals,
                                  select=select_callable,
                                  a_shape_vals=a_shape_vals)

  # Number of return values depends on value of sort_eig_vals.
  T, vs, *_, info = gees_result

  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")

  select_T_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
  T = _broadcasting_select_hlo(
      ctx,
      mlir.broadcast_in_dim(ctx, ok, select_T_aval,
                            broadcast_dimensions=range(len(batch_dims))),
      select_T_aval,
      T, ctx.avals_out[0],_nan_like_hlo(ctx, ctx.avals_out[0]), ctx.avals_out[0])
  output = [T]
  if compute_schur_vectors:
    select_vs_aval = ShapedArray(batch_dims + (1, 1), np.dtype(np.bool_))
    vs = _broadcasting_select_hlo(
        ctx,
        mlir.broadcast_in_dim(ctx, ok, select_vs_aval,
                              broadcast_dimensions=range(len(batch_dims))),
        select_vs_aval,
        vs, ctx.avals_out[1], _nan_like_hlo(ctx, ctx.avals_out[1]), ctx.avals_out[1])

    output.append(vs)

  return output

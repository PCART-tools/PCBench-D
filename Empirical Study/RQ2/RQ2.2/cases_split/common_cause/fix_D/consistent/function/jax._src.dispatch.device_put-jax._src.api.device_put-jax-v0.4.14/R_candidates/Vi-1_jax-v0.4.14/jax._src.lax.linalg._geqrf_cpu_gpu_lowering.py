def _geqrf_cpu_gpu_lowering(geqrf_impl, batched_geqrf_impl, ctx, a, *,
                            platform: str):
  a_aval, taus_aval = ctx.avals_out
  *batch_dims, m, n = a_aval.shape
  # It should be possible to support fully-dynamic shapes, but since
  # the last two dimensions (m, n) are used in more involved ways, we only
  # support dynamic dimensions for the batch size for now.
  if not is_constant_shape([m, n]):
    raise NotImplementedError(
      "Shape polymorphism for native serialization for qr on CPU and GPU is "
      f"implemented only for the batch dimensions: {a_aval.shape}")
  batch = math.prod(batch_dims)

  if batch == 0 or m == 0 or n == 0:
    return mlir.full_like_aval(ctx, 0, a_aval), mlir.full_like_aval(ctx, 0, taus_aval)

  if not is_constant_shape(a_aval.shape):
    if platform in ["cuda", "rocm"] or jaxlib_version < (0, 4, 13):
      # TODO(necula): remove the platform kwarg when we implement GPU support.
      raise NotImplementedError(
          "Shape polymorphism for native serialization for QR is not "
          f"implemented, try to upgrade jaxlib; b/261671778; {a_aval.shape}")

  if (batched_geqrf_impl is not None and batch > 1 and m // batch <= 128 and
      n // batch <= 128):
    a_out, taus = batched_geqrf_impl(a_aval.dtype, a)
  else:
    if platform in ["cuda", "rocm"] or jaxlib_version < (0, 4, 13):
      a_out, taus, info_geqrf = geqrf_impl(a_aval.dtype, a)  # type: ignore
    else:
      a_shape_vals = mlir.eval_dynamic_shape_as_ivals(ctx, a_aval.shape)
      a_out, taus, info_geqrf = geqrf_impl(a_aval.dtype, a,
                                           a_shape_vals=a_shape_vals)
    zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
    ok = mlir.compare_hlo(info_geqrf, zeros, "EQ", "SIGNED")
    select_ok_a_aval = ShapedArray(batch_dims + [1, 1], np.dtype(np.bool_))
    ok_a = mlir.broadcast_in_dim(ctx, ok, select_ok_a_aval,
                                 broadcast_dimensions=range(len(batch_dims)))
    a_out = _broadcasting_select_hlo(ctx, ok_a, select_ok_a_aval, a_out, a_aval, _nan_like_hlo(ctx, a_aval), a_aval)
    select_ok_taus_aval = ShapedArray(batch_dims + [1], np.dtype(np.bool_))
    ok_taus = mlir.broadcast_in_dim(ctx, ok, select_ok_taus_aval,
                                    broadcast_dimensions=range(len(batch_dims)))
    taus = _broadcasting_select_hlo(ctx, ok_taus, select_ok_taus_aval, taus, taus_aval, _nan_like_hlo(ctx, taus_aval), taus_aval)
  return a_out, taus

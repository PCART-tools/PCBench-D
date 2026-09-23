def _fft_lowering_cpu(ctx, x, *, fft_type, fft_lengths):
  x_aval, = ctx.avals_in
  if jaxlib_version < (0, 4, 13):
    if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
      raise NotImplementedError("Shape polymorphism for custom call is not implemented (fft); b/261671778; try updating your jaxlib.")
    return [ducc_fft.ducc_fft_hlo(x, x_aval.dtype, fft_type=fft_type,  # type: ignore
                                  fft_lengths=fft_lengths)]

  in_shape = x_aval.shape
  dtype = x_aval.dtype
  out_aval, = ctx.avals_out
  out_shape = out_aval.shape

  forward = fft_type in (xla_client.FftType.FFT, xla_client.FftType.RFFT)
  ndims = len(in_shape)
  assert len(fft_lengths) >= 1
  assert len(fft_lengths) <= ndims, (fft_lengths, ndims)
  assert len(in_shape) == len(out_shape) == ndims

  # PocketFft does not allow size 0 dimensions.
  if 0 in in_shape or 0 in out_shape:
    if fft_type == xla_client.FftType.RFFT:
      assert dtype in (np.float32, np.float64), dtype
      out_dtype = np.dtype(np.complex64 if dtype == np.float32 else np.complex128)

    elif fft_type == xla_client.FftType.IRFFT:
      assert np.issubdtype(dtype, np.complexfloating), dtype
      out_dtype = np.dtype(np.float32 if dtype == np.complex64 else np.float64)

    else:
      assert np.issubdtype(dtype, np.complexfloating), dtype
      out_dtype = dtype

    zero = mlir.ir_constant(np.array(0, dtype=out_dtype))
    return [
        mlir.broadcast_in_dim(ctx, zero, out_aval, broadcast_dimensions=[])]

  strides_in = []
  stride = 1
  for d in reversed(in_shape):
    strides_in.append(stride)
    stride *= d
  strides_in = mlir.shape_tensor(
      mlir.eval_dynamic_shape(ctx, tuple(reversed(strides_in))))

  strides_out = []
  stride = 1
  for d in reversed(out_shape):
    strides_out.append(stride)
    stride *= d
  strides_out = mlir.shape_tensor(
      mlir.eval_dynamic_shape(ctx, tuple(reversed(strides_out))))

  # scale = 1. if forward else (1. / np.prod(fft_lengths)) as a f64[1] tensor
  double_type = mlir.ir.RankedTensorType.get((), mlir.ir.F64Type.get())
  size_fft_length_prod = np.prod(fft_lengths) if fft_lengths else 1
  size_fft_lengths, = mlir.eval_dynamic_shape_as_vals(ctx, (size_fft_length_prod,))
  size_fft_lengths = hlo.ConvertOp(double_type, size_fft_lengths)
  one = mlir.ir_constant(np.float64(1.))
  scale = one if forward else hlo.DivOp(one, size_fft_lengths)
  scale = hlo.ReshapeOp(
      mlir.ir.RankedTensorType.get((1,), mlir.ir.F64Type.get()),
      scale).result

  in_shape = mlir.shape_tensor(mlir.eval_dynamic_shape(ctx, in_shape))
  out_shape = mlir.shape_tensor(mlir.eval_dynamic_shape(ctx, out_shape))
  in_shape = in_shape if fft_type != xla_client.FftType.IRFFT else out_shape

  result_type = mlir.aval_to_ir_type(out_aval)
  return [ducc_fft.dynamic_ducc_fft_hlo(
      result_type, x,
      input_dtype=x_aval.dtype, ndims=ndims, input_shape=in_shape,
      strides_in=strides_in, strides_out=strides_out, scale=scale,
      fft_type=fft_type, fft_lengths=fft_lengths, result_shape=out_shape)]

def _fft_lowering_cpu(ctx, x, *, fft_type, fft_lengths):
  if any(not is_constant_shape(a.shape) for a in (ctx.avals_in + ctx.avals_out)):
    raise NotImplementedError("Shape polymorphism for custom call is not implemented (fft); b/261671778")
  x_aval, = ctx.avals_in
  return [ducc_fft.ducc_fft_hlo(x, x_aval.dtype, fft_type=fft_type,
                                fft_lengths=fft_lengths)]

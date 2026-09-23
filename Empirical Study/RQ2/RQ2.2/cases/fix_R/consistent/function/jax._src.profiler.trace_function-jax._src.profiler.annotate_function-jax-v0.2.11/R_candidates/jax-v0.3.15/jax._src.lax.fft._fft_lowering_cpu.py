def _fft_lowering_cpu(ctx, x, *, fft_type, fft_lengths):
  x_aval, = ctx.avals_in
  return [pocketfft.pocketfft_mhlo(x, x_aval.dtype, fft_type=fft_type,
                                   fft_lengths=fft_lengths)]

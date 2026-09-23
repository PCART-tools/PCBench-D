def _fft_lowering(ctx, x, *, fft_type, fft_lengths):
  return [
      hlo.FftOp(x, hlo.FftTypeAttr.get(fft_type.name),
                mlir.dense_int_elements(fft_lengths)).result
  ]

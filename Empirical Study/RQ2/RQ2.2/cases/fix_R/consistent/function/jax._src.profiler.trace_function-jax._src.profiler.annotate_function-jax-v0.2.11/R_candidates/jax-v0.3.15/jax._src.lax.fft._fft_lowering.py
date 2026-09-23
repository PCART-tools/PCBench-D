def _fft_lowering(ctx, x, *, fft_type, fft_lengths):
  out_aval, = ctx.avals_out
  return [mhlo.FftOp(mlir.aval_to_ir_type(out_aval), x,
                     mhlo.FftTypeAttr.get(fft_type.name),
                     mlir.dense_int_elements(fft_lengths)).result]

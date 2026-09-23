@partial(jit, static_argnums=1)
def _rfft_transpose(t, fft_lengths):
  # The transpose of RFFT can't be expressed only in terms of irfft. Instead of
  # manually building up larger twiddle matrices (which would increase the
  # asymptotic complexity and is also rather complicated), we rely JAX to
  # transpose a naive RFFT implementation.
  dummy_shape = t.shape[:-len(fft_lengths)] + fft_lengths
  dummy_primal = ShapeDtypeStruct(dummy_shape, _real_dtype(t.dtype))
  transpose = linear_transpose(
      partial(_naive_rfft, fft_lengths=fft_lengths), dummy_primal)
  result, = transpose(t)
  assert result.dtype == _real_dtype(t.dtype), (result.dtype, t.dtype)
  return result

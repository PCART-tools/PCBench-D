def _irfft_transpose(t, fft_lengths):
  # The transpose of IRFFT is the RFFT of the cotangent times a scaling
  # factor and a mask. The mask scales the cotangent for the Hermitian
  # symmetric components of the RFFT by a factor of two, since these components
  # are de-duplicated in the RFFT.
  x = fft(t, xla_client.FftType.RFFT, fft_lengths)
  n = x.shape[-1]
  is_odd = fft_lengths[-1] % 2
  full = partial(lax.full_like, t, dtype=x.dtype)
  mask = lax.concatenate(
      [full(1.0, shape=(1,)),
       full(2.0, shape=(n - 2 + is_odd,)),
       full(1.0, shape=(1 - is_odd,))],
      dimension=0)
  scale = 1 / math.prod(fft_lengths)
  out = scale * lax.expand_dims(mask, range(x.ndim - 1)) * x
  assert out.dtype == _complex_dtype(t.dtype), (out.dtype, t.dtype)
  # Use JAX's convention for complex gradients
  # https://github.com/google/jax/issues/6223#issuecomment-807740707
  return lax.conj(out)

@partial(jit, static_argnums=(1, 2))
def fft(x, fft_type: Union[xla_client.FftType, str], fft_lengths: Sequence[int]):
  if isinstance(fft_type, str):
    typ = _str_to_fft_type(fft_type)
  elif isinstance(fft_type, xla_client.FftType):
    typ = fft_type
  else:
    raise TypeError(f"Unknown FFT type value '{fft_type}'")

  if typ == xla_client.FftType.RFFT:
    if np.iscomplexobj(x):
      raise ValueError("only real valued inputs supported for rfft")
    x, = promote_dtypes_inexact(x)
  else:
    x, = promote_dtypes_complex(x)
  if len(fft_lengths) == 0:
    # XLA FFT doesn't support 0-rank.
    return x
  fft_lengths = tuple(fft_lengths)
  return fft_p.bind(x, fft_type=typ, fft_lengths=fft_lengths)

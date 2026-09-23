def fft_abstract_eval(x, fft_type, fft_lengths):
  if len(fft_lengths) > x.ndim:
    raise ValueError(f"FFT input shape {x.shape} must have at least as many "
                    f"input dimensions as fft_lengths {fft_lengths}.")
  if fft_type == xla_client.FftType.RFFT:
    if x.shape[-len(fft_lengths):] != fft_lengths:
      raise ValueError(f"RFFT input shape {x.shape} minor dimensions must "
                      f"be equal to fft_lengths {fft_lengths}")
    shape = (x.shape[:-len(fft_lengths)] + fft_lengths[:-1]
             + (fft_lengths[-1] // 2 + 1,))
    dtype = _complex_dtype(x.dtype)
  elif fft_type == xla_client.FftType.IRFFT:
    if x.shape[-len(fft_lengths):-1] != fft_lengths[:-1]:
      raise ValueError(f"IRFFT input shape {x.shape} minor dimensions must "
                      "be equal to all except the last fft_length, got "
                      f"{fft_lengths=}")
    shape = x.shape[:-len(fft_lengths)] + fft_lengths
    dtype = _real_dtype(x.dtype)
  else:
    if x.shape[-len(fft_lengths):] != fft_lengths:
      raise ValueError(f"FFT input shape {x.shape} minor dimensions must "
                      f"be equal to fft_lengths {fft_lengths}")
    shape = x.shape
    dtype = x.dtype
  return x.update(shape=shape, dtype=dtype)

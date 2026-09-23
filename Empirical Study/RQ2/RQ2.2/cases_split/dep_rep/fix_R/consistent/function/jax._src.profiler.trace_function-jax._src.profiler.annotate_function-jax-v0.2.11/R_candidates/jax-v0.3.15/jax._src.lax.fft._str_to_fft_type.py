def _str_to_fft_type(s: str) -> xla_client.FftType:
  if s == "FFT":
    return xla_client.FftType.FFT
  elif s == "IFFT":
    return xla_client.FftType.IFFT
  elif s == "RFFT":
    return xla_client.FftType.RFFT
  elif s == "IRFFT":
    return xla_client.FftType.IRFFT
  else:
    raise ValueError(f"Unknown FFT type '{s}'")

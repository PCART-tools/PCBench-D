def _naive_rfft(x, fft_lengths):
  y = fft(x, xla_client.FftType.FFT, fft_lengths)
  n = fft_lengths[-1]
  return y[..., : n//2 + 1]

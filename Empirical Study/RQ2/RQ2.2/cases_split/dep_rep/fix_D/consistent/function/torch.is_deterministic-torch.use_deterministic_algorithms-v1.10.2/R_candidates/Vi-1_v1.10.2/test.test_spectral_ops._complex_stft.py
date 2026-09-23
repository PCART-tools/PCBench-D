def _complex_stft(x, *args, **kwargs):
    # Transform real and imaginary components separably
    stft_real = torch.stft(x.real, *args, **kwargs, return_complex=True, onesided=False)
    stft_imag = torch.stft(x.imag, *args, **kwargs, return_complex=True, onesided=False)
    return stft_real + 1j * stft_imag

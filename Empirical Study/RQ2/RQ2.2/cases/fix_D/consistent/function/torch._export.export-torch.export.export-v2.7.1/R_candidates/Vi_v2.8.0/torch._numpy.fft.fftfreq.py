@normalizer
def fftfreq(n, d=1.0):
    return torch.fft.fftfreq(n, d)

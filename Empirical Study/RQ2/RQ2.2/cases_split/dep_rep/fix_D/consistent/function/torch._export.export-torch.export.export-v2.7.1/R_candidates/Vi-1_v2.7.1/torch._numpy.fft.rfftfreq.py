@normalizer
def rfftfreq(n, d=1.0):
    return torch.fft.rfftfreq(n, d)

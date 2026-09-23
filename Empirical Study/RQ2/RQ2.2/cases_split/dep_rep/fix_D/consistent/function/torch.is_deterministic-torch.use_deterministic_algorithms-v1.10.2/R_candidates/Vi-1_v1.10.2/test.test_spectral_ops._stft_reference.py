def _stft_reference(x, hop_length, window):
    r"""Reference stft implementation

    This doesn't implement all of torch.stft, only the STFT definition:

    .. math:: X(m, \omega) = \sum_n x[n]w[n - m] e^{-jn\omega}

    """
    n_fft = window.numel()
    X = torch.empty((n_fft, (x.numel() - n_fft + hop_length) // hop_length),
                    device=x.device, dtype=torch.cdouble)
    for m in range(X.size(1)):
        start = m * hop_length
        if start + n_fft > x.numel():
            slc = torch.empty(n_fft, device=x.device, dtype=x.dtype)
            tmp = x[start:]
            slc[:tmp.numel()] = tmp
        else:
            slc = x[start: start + n_fft]
        X[:, m] = torch.fft.fft(slc * window)
    return X

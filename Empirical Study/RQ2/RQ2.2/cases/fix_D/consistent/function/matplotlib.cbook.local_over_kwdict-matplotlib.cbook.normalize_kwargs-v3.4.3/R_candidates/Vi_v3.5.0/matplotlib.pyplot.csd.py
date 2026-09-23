@_copy_docstring_and_deprecators(Axes.csd)
def csd(
        x, y, NFFT=None, Fs=None, Fc=None, detrend=None, window=None,
        noverlap=None, pad_to=None, sides=None, scale_by_freq=None,
        return_line=None, *, data=None, **kwargs):
    return gca().csd(
        x, y, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend, window=window,
        noverlap=noverlap, pad_to=pad_to, sides=sides,
        scale_by_freq=scale_by_freq, return_line=return_line,
        **({"data": data} if data is not None else {}), **kwargs)

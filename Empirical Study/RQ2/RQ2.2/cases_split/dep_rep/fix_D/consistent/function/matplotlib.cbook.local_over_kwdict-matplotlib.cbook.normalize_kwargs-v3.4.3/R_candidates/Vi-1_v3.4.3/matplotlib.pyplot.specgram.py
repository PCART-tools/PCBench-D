@_copy_docstring_and_deprecators(Axes.specgram)
def specgram(
        x, NFFT=None, Fs=None, Fc=None, detrend=None, window=None,
        noverlap=None, cmap=None, xextent=None, pad_to=None,
        sides=None, scale_by_freq=None, mode=None, scale=None,
        vmin=None, vmax=None, *, data=None, **kwargs):
    __ret = gca().specgram(
        x, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend, window=window,
        noverlap=noverlap, cmap=cmap, xextent=xextent, pad_to=pad_to,
        sides=sides, scale_by_freq=scale_by_freq, mode=mode,
        scale=scale, vmin=vmin, vmax=vmax,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret[-1])
    return __ret

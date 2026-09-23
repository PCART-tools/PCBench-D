@_copy_docstring_and_deprecators(Axes.cohere)
def cohere(
        x, y, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
        window=mlab.window_hanning, noverlap=0, pad_to=None,
        sides='default', scale_by_freq=None, *, data=None, **kwargs):
    return gca().cohere(
        x, y, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend, window=window,
        noverlap=noverlap, pad_to=pad_to, sides=sides,
        scale_by_freq=scale_by_freq,
        **({"data": data} if data is not None else {}), **kwargs)

@_copy_docstring_and_deprecators(Axes.magnitude_spectrum)
def magnitude_spectrum(
        x, Fs=None, Fc=None, window=None, pad_to=None, sides=None,
        scale=None, *, data=None, **kwargs):
    return gca().magnitude_spectrum(
        x, Fs=Fs, Fc=Fc, window=window, pad_to=pad_to, sides=sides,
        scale=scale, **({"data": data} if data is not None else {}),
        **kwargs)

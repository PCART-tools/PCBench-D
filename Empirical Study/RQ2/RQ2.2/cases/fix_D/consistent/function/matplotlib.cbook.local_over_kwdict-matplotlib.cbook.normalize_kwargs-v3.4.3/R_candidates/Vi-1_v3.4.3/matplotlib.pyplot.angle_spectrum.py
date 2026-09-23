@_copy_docstring_and_deprecators(Axes.angle_spectrum)
def angle_spectrum(
        x, Fs=None, Fc=None, window=None, pad_to=None, sides=None, *,
        data=None, **kwargs):
    return gca().angle_spectrum(
        x, Fs=Fs, Fc=Fc, window=window, pad_to=pad_to, sides=sides,
        **({"data": data} if data is not None else {}), **kwargs)

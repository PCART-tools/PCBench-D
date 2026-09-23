@_copy_docstring_and_deprecators(Axes.xcorr)
def xcorr(
        x, y, normed=True, detrend=mlab.detrend_none, usevlines=True,
        maxlags=10, *, data=None, **kwargs):
    return gca().xcorr(
        x, y, normed=normed, detrend=detrend, usevlines=usevlines,
        maxlags=maxlags,
        **({"data": data} if data is not None else {}), **kwargs)

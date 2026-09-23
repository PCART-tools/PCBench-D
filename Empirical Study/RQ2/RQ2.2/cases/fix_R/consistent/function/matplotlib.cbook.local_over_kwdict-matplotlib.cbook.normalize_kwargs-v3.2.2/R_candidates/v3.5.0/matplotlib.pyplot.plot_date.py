@_copy_docstring_and_deprecators(Axes.plot_date)
def plot_date(
        x, y, fmt='o', tz=None, xdate=True, ydate=False, *,
        data=None, **kwargs):
    return gca().plot_date(
        x, y, fmt=fmt, tz=tz, xdate=xdate, ydate=ydate,
        **({"data": data} if data is not None else {}), **kwargs)

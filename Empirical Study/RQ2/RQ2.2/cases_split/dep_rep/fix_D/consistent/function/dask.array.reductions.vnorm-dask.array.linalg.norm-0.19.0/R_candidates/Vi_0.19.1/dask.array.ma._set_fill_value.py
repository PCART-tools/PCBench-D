def _set_fill_value(x, fill_value):
    if isinstance(x, np.ma.masked_array):
        x = x.copy()
        np.ma.set_fill_value(x, fill_value=fill_value)
    return x

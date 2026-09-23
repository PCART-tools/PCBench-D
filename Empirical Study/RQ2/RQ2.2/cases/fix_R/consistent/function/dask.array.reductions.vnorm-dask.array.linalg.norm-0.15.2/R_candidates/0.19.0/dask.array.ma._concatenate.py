@concatenate_lookup.register(np.ma.masked_array)
def _concatenate(arrays, axis=0):
    out = np.ma.concatenate(arrays, axis=axis)
    fill_values = [i.fill_value for i in arrays if hasattr(i, 'fill_value')]
    if any(isinstance(f, np.ndarray) for f in fill_values):
        raise ValueError("Dask doesn't support masked array's with "
                         "non-scalar `fill_value`s")
    if fill_values:
        # If all the fill_values are the same copy over the fill value
        fill_values = np.unique(fill_values)
        if len(fill_values) == 1:
            out.fill_value = fill_values[0]
    return out

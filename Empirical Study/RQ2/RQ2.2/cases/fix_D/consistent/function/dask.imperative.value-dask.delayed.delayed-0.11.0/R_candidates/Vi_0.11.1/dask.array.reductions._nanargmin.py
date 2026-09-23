def _nanargmin(x, axis, **kwargs):
    try:
        return chunk.nanargmin(x, axis, **kwargs)
    except ValueError:
        return chunk.nanargmin(np.where(np.isnan(x), np.inf, x), axis, **kwargs)

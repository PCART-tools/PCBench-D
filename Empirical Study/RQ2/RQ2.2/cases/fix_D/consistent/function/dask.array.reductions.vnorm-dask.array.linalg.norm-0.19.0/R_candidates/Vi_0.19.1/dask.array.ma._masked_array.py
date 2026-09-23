def _masked_array(data, mask=np.ma.nomask, **kwargs):
    dtype = kwargs.pop('masked_dtype', None)
    return np.ma.masked_array(data, mask=mask, dtype=dtype, **kwargs)

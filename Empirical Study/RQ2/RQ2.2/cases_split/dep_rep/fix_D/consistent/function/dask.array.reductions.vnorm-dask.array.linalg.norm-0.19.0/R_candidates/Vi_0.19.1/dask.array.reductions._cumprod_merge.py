def _cumprod_merge(a, b):
    if isinstance(a, np.ma.masked_array) or isinstance(b, np.ma.masked_array):
        values = np.ma.getdata(a) * np.ma.getdata(b)
        return np.ma.masked_array(values, mask=np.ma.getmaskarray(b))
    return a * b

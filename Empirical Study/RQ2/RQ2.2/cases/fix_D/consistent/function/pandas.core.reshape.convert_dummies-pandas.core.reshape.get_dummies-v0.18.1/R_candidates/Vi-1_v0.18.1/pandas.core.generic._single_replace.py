def _single_replace(self, to_replace, method, inplace, limit):
    if self.ndim != 1:
        raise TypeError('cannot replace {0} with method {1} on a {2}'
                        .format(to_replace, method, type(self).__name__))

    orig_dtype = self.dtype
    result = self if inplace else self.copy()
    fill_f = missing.get_fill_func(method)

    mask = missing.mask_missing(result.values, to_replace)
    values = fill_f(result.values, limit=limit, mask=mask)

    if values.dtype == orig_dtype and inplace:
        return

    result = pd.Series(values, index=self.index,
                       dtype=self.dtype).__finalize__(self)

    if inplace:
        self._update_inplace(result._data)
        return

    return result

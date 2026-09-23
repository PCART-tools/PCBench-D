    def transform(self, func, *args, **kwargs):
        """
        Call function producing a like-indexed Series on each group and return
        a Series with the transformed values

        Parameters
        ----------
        func : function
            To apply to each group. Should return a Series with the same index

        Examples
        --------
        >>> grouped.transform(lambda x: (x - x.mean()) / x.std())

        Returns
        -------
        transformed : Series
        """
        result = self._selected_obj.copy()
        if hasattr(result, 'values'):
            result = result.values
        dtype = result.dtype

        if isinstance(func, compat.string_types):
            wrapper = lambda x: getattr(x, func)(*args, **kwargs)
        else:
            wrapper = lambda x: func(x, *args, **kwargs)

        for name, group in self:

            object.__setattr__(group, 'name', name)
            res = wrapper(group)
            if hasattr(res, 'values'):
                res = res.values

            # need to do a safe put here, as the dtype may be different
            # this needs to be an ndarray
            result = Series(result)
            result.iloc[self._get_index(name)] = res
            result = result.values

        # downcast if we can (and need)
        result = _possibly_downcast_to_dtype(result, dtype)
        return self._selected_obj.__class__(result, index=self._selected_obj.index,
                                  name=self._selected_obj.name)

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

        func = self._is_cython_func(func) or func

        # if string function
        if isinstance(func, compat.string_types):
            if func in _cython_transforms:
                # cythonized transform
                return getattr(self, func)(*args, **kwargs)
            else:
                # cythonized aggregation and merge
                return self._transform_fast(
                    lambda: getattr(self, func)(*args, **kwargs))

        # reg transform
        dtype = self._selected_obj.dtype
        result = self._selected_obj.values.copy()

        wrapper = lambda x: func(x, *args, **kwargs)
        for i, (name, group) in enumerate(self):
            object.__setattr__(group, 'name', name)
            res = wrapper(group)

            if hasattr(res, 'values'):
                res = res.values

            # may need to astype
            try:
                common_type = np.common_type(np.array(res), result)
                if common_type != result.dtype:
                    result = result.astype(common_type)
            except:
                pass

            indexer = self._get_index(name)
            result[indexer] = res

        result = _possibly_downcast_to_dtype(result, dtype)
        return self._selected_obj.__class__(result,
                                            index=self._selected_obj.index,
                                            name=self._selected_obj.name)

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
        dtype = self._selected_obj.dtype

        if isinstance(func, compat.string_types):
            wrapper = lambda x: getattr(x, func)(*args, **kwargs)
        else:
            wrapper = lambda x: func(x, *args, **kwargs)

        result = self._selected_obj.values.copy()
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

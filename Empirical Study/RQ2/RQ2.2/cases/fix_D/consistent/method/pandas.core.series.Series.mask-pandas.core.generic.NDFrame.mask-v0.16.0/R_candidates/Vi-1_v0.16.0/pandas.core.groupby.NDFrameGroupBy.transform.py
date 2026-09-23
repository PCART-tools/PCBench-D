    def transform(self, func, *args, **kwargs):
        """
        Call function producing a like-indexed DataFrame on each group and
        return a DataFrame having the same indexes as the original object
        filled with the transformed values

        Parameters
        ----------
        f : function
            Function to apply to each subframe

        Notes
        -----
        Each subframe is endowed the attribute 'name' in case you need to know
        which group you are working on.

        Examples
        --------
        >>> grouped = df.groupby(lambda x: mapping[x])
        >>> grouped.transform(lambda x: (x - x.mean()) / x.std())
        """

        # try to do a fast transform via merge if possible
        try:
            obj = self._obj_with_exclusions
            if isinstance(func, compat.string_types):
                result = getattr(self, func)(*args, **kwargs)
            else:
                cyfunc = _intercept_cython(func)
                if cyfunc and not args and not kwargs:
                    result = getattr(self, cyfunc)()
                else:
                    return self._transform_general(func, *args, **kwargs)
        except:
            return self._transform_general(func, *args, **kwargs)

        # a reduction transform
        if not isinstance(result, DataFrame):
            return self._transform_general(func, *args, **kwargs)

        # nuiscance columns
        if not result.columns.equals(obj.columns):
            return self._transform_general(func, *args, **kwargs)

        # a grouped that doesn't preserve the index, remap index based on the grouper
        # and broadcast it
        if ((not isinstance(obj.index,MultiIndex) and
             type(result.index) != type(obj.index)) or
            len(result.index) != len(obj.index)):
            results = obj.values.copy()
            indices = self.indices
            for (name, group), (i, row) in zip(self, result.iterrows()):
                indexer = indices[name]
                results[indexer] = np.tile(row.values,len(indexer)).reshape(len(indexer),-1)
            return DataFrame(results,columns=result.columns,index=obj.index).convert_objects()

        # we can merge the result in
        # GH 7383
        names = result.columns
        result = obj.merge(result, how='outer', left_index=True, right_index=True).iloc[:,-result.shape[1]:]
        result.columns = names
        return result

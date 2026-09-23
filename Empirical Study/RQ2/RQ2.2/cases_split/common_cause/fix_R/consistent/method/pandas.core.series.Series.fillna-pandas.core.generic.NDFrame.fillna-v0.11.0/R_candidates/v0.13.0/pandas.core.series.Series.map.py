    def map(self, arg, na_action=None):
        """
        Map values of Series using input correspondence (which can be
        a dict, Series, or function)

        Parameters
        ----------
        arg : function, dict, or Series
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values

        Examples
        --------
        >>> x
        one   1
        two   2
        three 3

        >>> y
        1  foo
        2  bar
        3  baz

        >>> x.map(y)
        one   foo
        two   bar
        three baz

        Returns
        -------
        y : Series
            same index as caller
        """
        values = self.values
        if com.is_datetime64_dtype(values.dtype):
            values = lib.map_infer(values, lib.Timestamp)

        if na_action == 'ignore':
            mask = isnull(values)

            def map_f(values, f):
                return lib.map_infer_mask(values, f, mask.view(pa.uint8))
        else:
            map_f = lib.map_infer

        if isinstance(arg, (dict, Series)):
            if isinstance(arg, dict):
                arg = self._constructor(arg)

            indexer = arg.index.get_indexer(values)
            new_values = com.take_1d(arg.values, indexer)
            return self._constructor(new_values,
                                     index=self.index).__finalize__(self)
        else:
            mapped = map_f(values, arg)
            return self._constructor(mapped,
                                     index=self.index).__finalize__(self)

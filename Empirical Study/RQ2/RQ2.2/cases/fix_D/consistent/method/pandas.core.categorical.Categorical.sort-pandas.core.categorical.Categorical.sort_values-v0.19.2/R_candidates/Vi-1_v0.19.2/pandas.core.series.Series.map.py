    def map(self, arg, na_action=None):
        """
        Map values of Series using input correspondence (which can be
        a dict, Series, or function)

        Parameters
        ----------
        arg : function, dict, or Series
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values, without passing them to the
            mapping function

        Returns
        -------
        y : Series
            same index as caller

        Examples
        --------

        Map inputs to outputs

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

        Use na_action to control whether NA values are affected by the mapping
        function.

        >>> s = pd.Series([1, 2, 3, np.nan])

        >>> s2 = s.map(lambda x: 'this is a string {}'.format(x),
                       na_action=None)
        0    this is a string 1.0
        1    this is a string 2.0
        2    this is a string 3.0
        3    this is a string nan
        dtype: object

        >>> s3 = s.map(lambda x: 'this is a string {}'.format(x),
                       na_action='ignore')
        0    this is a string 1.0
        1    this is a string 2.0
        2    this is a string 3.0
        3                     NaN
        dtype: object

        """

        if is_extension_type(self.dtype):
            values = self._values
            if na_action is not None:
                raise NotImplementedError
            map_f = lambda values, f: values.map(f)
        else:
            values = self.asobject

            if na_action == 'ignore':
                def map_f(values, f):
                    return lib.map_infer_mask(values, f,
                                              isnull(values).view(np.uint8))
            else:
                map_f = lib.map_infer

        if isinstance(arg, (dict, Series)):
            if isinstance(arg, dict):
                arg = self._constructor(arg, index=arg.keys())

            indexer = arg.index.get_indexer(values)
            new_values = algos.take_1d(arg._values, indexer)
        else:
            new_values = map_f(values, arg)

        return self._constructor(new_values,
                                 index=self.index).__finalize__(self)

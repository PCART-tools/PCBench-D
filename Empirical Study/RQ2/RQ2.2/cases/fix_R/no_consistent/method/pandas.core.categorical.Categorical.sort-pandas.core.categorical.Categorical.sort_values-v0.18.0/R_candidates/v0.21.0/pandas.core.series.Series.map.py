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

        Map inputs to outputs (both of type `Series`)

        >>> x = pd.Series([1,2,3], index=['one', 'two', 'three'])
        >>> x
        one      1
        two      2
        three    3
        dtype: int64

        >>> y = pd.Series(['foo', 'bar', 'baz'], index=[1,2,3])
        >>> y
        1    foo
        2    bar
        3    baz

        >>> x.map(y)
        one   foo
        two   bar
        three baz

        If `arg` is a dictionary, return a new Series with values converted
        according to the dictionary's mapping:

        >>> z = {1: 'A', 2: 'B', 3: 'C'}

        >>> x.map(z)
        one   A
        two   B
        three C

        Use na_action to control whether NA values are affected by the mapping
        function.

        >>> s = pd.Series([1, 2, 3, np.nan])

        >>> s2 = s.map('this is a string {}'.format, na_action=None)
        0    this is a string 1.0
        1    this is a string 2.0
        2    this is a string 3.0
        3    this is a string nan
        dtype: object

        >>> s3 = s.map('this is a string {}'.format, na_action='ignore')
        0    this is a string 1.0
        1    this is a string 2.0
        2    this is a string 3.0
        3                     NaN
        dtype: object

        See Also
        --------
        Series.apply: For applying more complex functions on a Series
        DataFrame.apply: Apply a function row-/column-wise
        DataFrame.applymap: Apply a function elementwise on a whole DataFrame

        Notes
        -----
        When `arg` is a dictionary, values in Series that are not in the
        dictionary (as keys) are converted to ``NaN``. However, if the
        dictionary is a ``dict`` subclass that defines ``__missing__`` (i.e.
        provides a method for default values), then this default is used
        rather than ``NaN``:

        >>> from collections import Counter
        >>> counter = Counter()
        >>> counter['bar'] += 1
        >>> y.map(counter)
        1    0
        2    1
        3    0
        dtype: int64
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
                                              isna(values).view(np.uint8))
            else:
                map_f = lib.map_infer

        if isinstance(arg, dict):
            if hasattr(arg, '__missing__'):
                # If a dictionary subclass defines a default value method,
                # convert arg to a lookup function (GH #15999).
                dict_with_default = arg
                arg = lambda x: dict_with_default[x]
            else:
                # Dictionary does not have a default. Thus it's safe to
                # convert to an indexed series for efficiency.
                arg = self._constructor(arg, index=arg.keys())

        if isinstance(arg, Series):
            # arg is a Series
            indexer = arg.index.get_indexer(values)
            new_values = algorithms.take_1d(arg._values, indexer)
        else:
            # arg is a function
            new_values = map_f(values, arg)

        return self._constructor(new_values,
                                 index=self.index).__finalize__(self)

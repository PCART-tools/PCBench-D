    def map(self, arg, na_action=None):
        """
        Map values of Series using input correspondence (a dict, Series, or
        function).

        Parameters
        ----------
        arg : function, dict, or Series
            Mapping correspondence.
        na_action : {None, 'ignore'}
            If 'ignore', propagate NA values, without passing them to the
            mapping correspondence.

        Returns
        -------
        y : Series
            Same index as caller.

        Examples
        --------

        Map inputs to outputs (both of type `Series`):

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
        Series.apply : For applying more complex functions on a Series.
        DataFrame.apply : Apply a function row-/column-wise.
        DataFrame.applymap : Apply a function elementwise on a whole DataFrame.

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
        new_values = super(Series, self)._map_values(
            arg, na_action=na_action)
        return self._constructor(new_values,
                                 index=self.index).__finalize__(self)

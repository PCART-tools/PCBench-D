    def isin(self, values):
        """
        Return a boolean :class:`~pandas.Series` showing whether each element
        in the :class:`~pandas.Series` is exactly contained in the passed
        sequence of ``values``.

        Parameters
        ----------
        values : set or list-like
            The sequence of values to test. Passing in a single string will
            raise a ``TypeError``. Instead, turn a single string into a
            ``list`` of one element.

            .. versionadded:: 0.18.1

            Support for values as a set

        Returns
        -------
        isin : Series (bool dtype)

        Raises
        ------
        TypeError
          * If ``values`` is a string

        See Also
        --------
        pandas.DataFrame.isin

        Examples
        --------

        >>> s = pd.Series(list('abc'))
        >>> s.isin(['a', 'c', 'e'])
        0     True
        1    False
        2     True
        dtype: bool

        Passing a single string as ``s.isin('a')`` will raise an error. Use
        a list of one element instead:

        >>> s.isin(['a'])
        0     True
        1    False
        2    False
        dtype: bool

        """
        result = algos.isin(_values_from_object(self), values)
        return self._constructor(result, index=self.index).__finalize__(self)

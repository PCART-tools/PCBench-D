    @deprecate_kwarg(old_arg_name='n', new_arg_name='repeats')
    def repeat(self, repeats, *args, **kwargs):
        """
        Repeat elements of an Index.

        Returns a new index where each element of the current index
        is repeated consecutively a given number of times.

        Parameters
        ----------
        repeats : int
            The number of repetitions for each element.
        **kwargs
            Additional keywords have no effect but might be accepted for
            compatibility with numpy.

        Returns
        -------
        pandas.Index
            Newly created Index with repeated elements.

        See Also
        --------
        Series.repeat : Equivalent function for Series
        numpy.repeat : Underlying implementation

        Examples
        --------
        >>> idx = pd.Index([1, 2, 3])
        >>> idx
        Int64Index([1, 2, 3], dtype='int64')
        >>> idx.repeat(2)
        Int64Index([1, 1, 2, 2, 3, 3], dtype='int64')
        >>> idx.repeat(3)
        Int64Index([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype='int64')
        """
        nv.validate_repeat(args, kwargs)
        return self._shallow_copy(self._values.repeat(repeats))

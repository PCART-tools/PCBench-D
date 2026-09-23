    def select_dtypes(self, include=None, exclude=None):
        """Return a subset of a DataFrame including/excluding columns based on
        their ``dtype``.

        Parameters
        ----------
        include, exclude : scalar or list-like
            A selection of dtypes or strings to be included/excluded. At least
            one of these parameters must be supplied.

        Raises
        ------
        ValueError
            * If both of ``include`` and ``exclude`` are empty
            * If ``include`` and ``exclude`` have overlapping elements
            * If any kind of string dtype is passed in.

        Returns
        -------
        subset : DataFrame
            The subset of the frame including the dtypes in ``include`` and
            excluding the dtypes in ``exclude``.

        Notes
        -----
        * To select all *numeric* types use the numpy dtype ``numpy.number``
        * To select strings you must use the ``object`` dtype, but note that
          this will return *all* object dtype columns
        * See the `numpy dtype hierarchy
          <http://docs.scipy.org/doc/numpy/reference/arrays.scalars.html>`__
        * To select datetimes, use np.datetime64, 'datetime' or 'datetime64'
        * To select timedeltas, use np.timedelta64, 'timedelta' or
          'timedelta64'
        * To select Pandas categorical dtypes, use 'category'
        * To select Pandas datetimetz dtypes, use 'datetimetz' (new in 0.20.0),
          or a 'datetime64[ns, tz]' string

        Examples
        --------
        >>> df = pd.DataFrame({'a': np.random.randn(6).astype('f4'),
        ...                    'b': [True, False] * 3,
        ...                    'c': [1.0, 2.0] * 3})
        >>> df
                a      b  c
        0  0.3962   True  1
        1  0.1459  False  2
        2  0.2623   True  1
        3  0.0764  False  2
        4 -0.9703   True  1
        5 -1.2094  False  2
        >>> df.select_dtypes(include='bool')
           c
        0  True
        1  False
        2  True
        3  False
        4  True
        5  False
        >>> df.select_dtypes(include=['float64'])
           c
        0  1
        1  2
        2  1
        3  2
        4  1
        5  2
        >>> df.select_dtypes(exclude=['floating'])
               b
        0   True
        1  False
        2   True
        3  False
        4   True
        5  False
        """

        if not is_list_like(include):
            include = (include,) if include is not None else ()
        if not is_list_like(exclude):
            exclude = (exclude,) if exclude is not None else ()

        selection = tuple(map(frozenset, (include, exclude)))

        if not any(selection):
            raise ValueError('at least one of include or exclude must be '
                             'nonempty')

        # convert the myriad valid dtypes object to a single representation
        include, exclude = map(
            lambda x: frozenset(map(_get_dtype_from_object, x)), selection)
        for dtypes in (include, exclude):
            invalidate_string_dtypes(dtypes)

        # can't both include AND exclude!
        if not include.isdisjoint(exclude):
            raise ValueError('include and exclude overlap on %s' %
                             (include & exclude))

        # empty include/exclude -> defaults to True
        # three cases (we've already raised if both are empty)
        # case 1: empty include, nonempty exclude
        # we have True, True, ... True for include, same for exclude
        # in the loop below we get the excluded
        # and when we call '&' below we get only the excluded
        # case 2: nonempty include, empty exclude
        # same as case 1, but with include
        # case 3: both nonempty
        # the "union" of the logic of case 1 and case 2:
        # we get the included and excluded, and return their logical and
        include_these = Series(not bool(include), index=self.columns)
        exclude_these = Series(not bool(exclude), index=self.columns)

        def is_dtype_instance_mapper(column, dtype):
            return column, functools.partial(issubclass, dtype.type)

        for column, f in itertools.starmap(is_dtype_instance_mapper,
                                           self.dtypes.iteritems()):
            if include:  # checks for the case of empty include or exclude
                include_these[column] = any(map(f, include))
            if exclude:
                exclude_these[column] = not any(map(f, exclude))

        dtype_indexer = include_these & exclude_these
        return self.loc[com._get_info_slice(self, dtype_indexer)]

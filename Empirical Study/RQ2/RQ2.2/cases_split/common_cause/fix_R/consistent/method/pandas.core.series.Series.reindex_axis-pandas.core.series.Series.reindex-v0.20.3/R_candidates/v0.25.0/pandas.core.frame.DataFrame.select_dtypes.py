    def select_dtypes(self, include=None, exclude=None):
        """
        Return a subset of the DataFrame's columns based on the column dtypes.

        Parameters
        ----------
        include, exclude : scalar or list-like
            A selection of dtypes or strings to be included/excluded. At least
            one of these parameters must be supplied.

        Returns
        -------
        DataFrame
            The subset of the frame including the dtypes in ``include`` and
            excluding the dtypes in ``exclude``.

        Raises
        ------
        ValueError
            * If both of ``include`` and ``exclude`` are empty
            * If ``include`` and ``exclude`` have overlapping elements
            * If any kind of string dtype is passed in.

        Notes
        -----
        * To select all *numeric* types, use ``np.number`` or ``'number'``
        * To select strings you must use the ``object`` dtype, but note that
          this will return *all* object dtype columns
        * See the `numpy dtype hierarchy
          <http://docs.scipy.org/doc/numpy/reference/arrays.scalars.html>`__
        * To select datetimes, use ``np.datetime64``, ``'datetime'`` or
          ``'datetime64'``
        * To select timedeltas, use ``np.timedelta64``, ``'timedelta'`` or
          ``'timedelta64'``
        * To select Pandas categorical dtypes, use ``'category'``
        * To select Pandas datetimetz dtypes, use ``'datetimetz'`` (new in
          0.20.0) or ``'datetime64[ns, tz]'``

        Examples
        --------
        >>> df = pd.DataFrame({'a': [1, 2] * 3,
        ...                    'b': [True, False] * 3,
        ...                    'c': [1.0, 2.0] * 3})
        >>> df
                a      b  c
        0       1   True  1.0
        1       2  False  2.0
        2       1   True  1.0
        3       2  False  2.0
        4       1   True  1.0
        5       2  False  2.0

        >>> df.select_dtypes(include='bool')
           b
        0  True
        1  False
        2  True
        3  False
        4  True
        5  False

        >>> df.select_dtypes(include=['float64'])
           c
        0  1.0
        1  2.0
        2  1.0
        3  2.0
        4  1.0
        5  2.0

        >>> df.select_dtypes(exclude=['int'])
               b    c
        0   True  1.0
        1  False  2.0
        2   True  1.0
        3  False  2.0
        4   True  1.0
        5  False  2.0
        """

        def _get_info_slice(obj, indexer):
            """Slice the info axis of `obj` with `indexer`."""
            if not hasattr(obj, "_info_axis_number"):
                msg = "object of type {typ!r} has no info axis"
                raise TypeError(msg.format(typ=type(obj).__name__))
            slices = [slice(None)] * obj.ndim
            slices[obj._info_axis_number] = indexer
            return tuple(slices)

        if not is_list_like(include):
            include = (include,) if include is not None else ()
        if not is_list_like(exclude):
            exclude = (exclude,) if exclude is not None else ()

        selection = tuple(map(frozenset, (include, exclude)))

        if not any(selection):
            raise ValueError("at least one of include or exclude must be " "nonempty")

        # convert the myriad valid dtypes object to a single representation
        include, exclude = map(
            lambda x: frozenset(map(infer_dtype_from_object, x)), selection
        )
        for dtypes in (include, exclude):
            invalidate_string_dtypes(dtypes)

        # can't both include AND exclude!
        if not include.isdisjoint(exclude):
            raise ValueError(
                "include and exclude overlap on {inc_ex}".format(
                    inc_ex=(include & exclude)
                )
            )

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

        def is_dtype_instance_mapper(idx, dtype):
            return idx, functools.partial(issubclass, dtype.type)

        for idx, f in itertools.starmap(
            is_dtype_instance_mapper, enumerate(self.dtypes)
        ):
            if include:  # checks for the case of empty include or exclude
                include_these.iloc[idx] = any(map(f, include))
            if exclude:
                exclude_these.iloc[idx] = not any(map(f, exclude))

        dtype_indexer = include_these & exclude_these
        return self.loc[_get_info_slice(self, dtype_indexer)]

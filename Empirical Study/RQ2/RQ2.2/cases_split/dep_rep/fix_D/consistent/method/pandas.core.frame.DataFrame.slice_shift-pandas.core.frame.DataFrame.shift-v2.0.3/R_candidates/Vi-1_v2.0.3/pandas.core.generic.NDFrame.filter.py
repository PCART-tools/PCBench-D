    def filter(
        self: NDFrameT,
        items=None,
        like: str | None = None,
        regex: str | None = None,
        axis: Axis | None = None,
    ) -> NDFrameT:
        """
        Subset the dataframe rows or columns according to the specified index labels.

        Note that this routine does not filter a dataframe on its
        contents. The filter is applied to the labels of the index.

        Parameters
        ----------
        items : list-like
            Keep labels from axis which are in items.
        like : str
            Keep labels from axis for which "like in label == True".
        regex : str (regular expression)
            Keep labels from axis for which re.search(regex, label) == True.
        axis : {0 or ‘index’, 1 or ‘columns’, None}, default None
            The axis to filter on, expressed either as an index (int)
            or axis name (str). By default this is the info axis, 'columns' for
            DataFrame. For `Series` this parameter is unused and defaults to `None`.

        Returns
        -------
        same type as input object

        See Also
        --------
        DataFrame.loc : Access a group of rows and columns
            by label(s) or a boolean array.

        Notes
        -----
        The ``items``, ``like``, and ``regex`` parameters are
        enforced to be mutually exclusive.

        ``axis`` defaults to the info axis that is used when indexing
        with ``[]``.

        Examples
        --------
        >>> df = pd.DataFrame(np.array(([1, 2, 3], [4, 5, 6])),
        ...                   index=['mouse', 'rabbit'],
        ...                   columns=['one', 'two', 'three'])
        >>> df
                one  two  three
        mouse     1    2      3
        rabbit    4    5      6

        >>> # select columns by name
        >>> df.filter(items=['one', 'three'])
                 one  three
        mouse     1      3
        rabbit    4      6

        >>> # select columns by regular expression
        >>> df.filter(regex='e$', axis=1)
                 one  three
        mouse     1      3
        rabbit    4      6

        >>> # select rows containing 'bbi'
        >>> df.filter(like='bbi', axis=0)
                 one  two  three
        rabbit    4    5      6
        """
        nkw = common.count_not_none(items, like, regex)
        if nkw > 1:
            raise TypeError(
                "Keyword arguments `items`, `like`, or `regex` "
                "are mutually exclusive"
            )

        if axis is None:
            axis = self._info_axis_name
        labels = self._get_axis(axis)

        if items is not None:
            name = self._get_axis_name(axis)
            # error: Keywords must be strings
            return self.reindex(  # type: ignore[misc]
                **{name: [r for r in items if r in labels]}  # type: ignore[arg-type]
            )
        elif like:

            def f(x) -> bool_t:
                assert like is not None  # needed for mypy
                return like in ensure_str(x)

            values = labels.map(f)
            return self.loc(axis=axis)[values]
        elif regex:

            def f(x) -> bool_t:
                return matcher.search(ensure_str(x)) is not None

            matcher = re.compile(regex)
            values = labels.map(f)
            return self.loc(axis=axis)[values]
        else:
            raise TypeError("Must pass either `items`, `like`, or `regex`")

    @final
    def rank(
        self: NDFrameT,
        axis=0,
        method: str = "average",
        numeric_only: bool_t | None | lib.NoDefault = lib.no_default,
        na_option: str = "keep",
        ascending: bool_t = True,
        pct: bool_t = False,
    ) -> NDFrameT:
        """
        Compute numerical data ranks (1 through n) along axis.

        By default, equal values are assigned a rank that is the average of the
        ranks of those values.

        Parameters
        ----------
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Index to direct ranking.
            For `Series` this parameter is unused and defaults to 0.
        method : {'average', 'min', 'max', 'first', 'dense'}, default 'average'
            How to rank the group of records that have the same value (i.e. ties):

            * average: average rank of the group
            * min: lowest rank in the group
            * max: highest rank in the group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups.

        numeric_only : bool, optional
            For DataFrame objects, rank only numeric columns if set to True.
        na_option : {'keep', 'top', 'bottom'}, default 'keep'
            How to rank NaN values:

            * keep: assign NaN rank to NaN values
            * top: assign lowest rank to NaN values
            * bottom: assign highest rank to NaN values

        ascending : bool, default True
            Whether or not the elements should be ranked in ascending order.
        pct : bool, default False
            Whether or not to display the returned rankings in percentile
            form.

        Returns
        -------
        same type as caller
            Return a Series or DataFrame with data ranks as values.

        See Also
        --------
        core.groupby.GroupBy.rank : Rank of values within each group.

        Examples
        --------
        >>> df = pd.DataFrame(data={'Animal': ['cat', 'penguin', 'dog',
        ...                                    'spider', 'snake'],
        ...                         'Number_legs': [4, 2, 4, 8, np.nan]})
        >>> df
            Animal  Number_legs
        0      cat          4.0
        1  penguin          2.0
        2      dog          4.0
        3   spider          8.0
        4    snake          NaN

        Ties are assigned the mean of the ranks (by default) for the group.

        >>> s = pd.Series(range(5), index=list("abcde"))
        >>> s["d"] = s["b"]
        >>> s.rank()
        a    1.0
        b    2.5
        c    4.0
        d    2.5
        e    5.0
        dtype: float64

        The following example shows how the method behaves with the above
        parameters:

        * default_rank: this is the default behaviour obtained without using
          any parameter.
        * max_rank: setting ``method = 'max'`` the records that have the
          same values are ranked using the highest rank (e.g.: since 'cat'
          and 'dog' are both in the 2nd and 3rd position, rank 3 is assigned.)
        * NA_bottom: choosing ``na_option = 'bottom'``, if there are records
          with NaN values they are placed at the bottom of the ranking.
        * pct_rank: when setting ``pct = True``, the ranking is expressed as
          percentile rank.

        >>> df['default_rank'] = df['Number_legs'].rank()
        >>> df['max_rank'] = df['Number_legs'].rank(method='max')
        >>> df['NA_bottom'] = df['Number_legs'].rank(na_option='bottom')
        >>> df['pct_rank'] = df['Number_legs'].rank(pct=True)
        >>> df
            Animal  Number_legs  default_rank  max_rank  NA_bottom  pct_rank
        0      cat          4.0           2.5       3.0        2.5     0.625
        1  penguin          2.0           1.0       1.0        1.0     0.250
        2      dog          4.0           2.5       3.0        2.5     0.625
        3   spider          8.0           4.0       4.0        4.0     1.000
        4    snake          NaN           NaN       NaN        5.0       NaN
        """
        warned = False
        if numeric_only is None:
            # GH#45036
            warnings.warn(
                f"'numeric_only=None' in {type(self).__name__}.rank is deprecated "
                "and will raise in a future version. Pass either 'True' or "
                "'False'. 'False' will be the default.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            warned = True
        elif numeric_only is lib.no_default:
            numeric_only = None

        axis = self._get_axis_number(axis)

        if na_option not in {"keep", "top", "bottom"}:
            msg = "na_option must be one of 'keep', 'top', or 'bottom'"
            raise ValueError(msg)

        def ranker(data):
            if data.ndim == 2:
                # i.e. DataFrame, we cast to ndarray
                values = data.values
            else:
                # i.e. Series, can dispatch to EA
                values = data._values

            if isinstance(values, ExtensionArray):
                ranks = values._rank(
                    axis=axis,
                    method=method,
                    ascending=ascending,
                    na_option=na_option,
                    pct=pct,
                )
            else:
                ranks = algos.rank(
                    values,
                    axis=axis,
                    method=method,
                    ascending=ascending,
                    na_option=na_option,
                    pct=pct,
                )

            ranks_obj = self._constructor(ranks, **data._construct_axes_dict())
            return ranks_obj.__finalize__(self, method="rank")

        # if numeric_only is None, and we can't get anything, we try with
        # numeric_only=True
        if numeric_only is None:
            try:
                return ranker(self)
            except TypeError:
                numeric_only = True
                if not warned:
                    # Only warn here if we didn't already issue a warning above
                    # GH#45036
                    warnings.warn(
                        f"Dropping of nuisance columns in {type(self).__name__}.rank "
                        "is deprecated; in a future version this will raise TypeError. "
                        "Select only valid columns before calling rank.",
                        FutureWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )

        if numeric_only:
            if self.ndim == 1 and not is_numeric_dtype(self.dtype):
                # GH#47500
                warnings.warn(
                    f"Calling Series.rank with numeric_only={numeric_only} and dtype "
                    f"{self.dtype} is deprecated and will raise a TypeError in a "
                    "future version of pandas",
                    category=FutureWarning,
                    stacklevel=find_stack_level(inspect.currentframe()),
                )
            data = self._get_numeric_data()
        else:
            data = self

        return ranker(data)

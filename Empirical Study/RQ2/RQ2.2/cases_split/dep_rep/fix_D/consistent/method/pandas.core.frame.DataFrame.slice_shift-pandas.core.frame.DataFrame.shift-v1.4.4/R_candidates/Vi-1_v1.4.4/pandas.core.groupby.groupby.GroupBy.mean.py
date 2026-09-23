    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def mean(
        self,
        numeric_only: bool | lib.NoDefault = lib.no_default,
        engine: str = "cython",
        engine_kwargs: dict[str, bool] | None = None,
    ):
        """
        Compute mean of groups, excluding missing values.

        Parameters
        ----------
        numeric_only : bool, default True
            Include only float, int, boolean columns. If None, will attempt to use
            everything, then use only numeric data.

        engine : str, default None
            * ``'cython'`` : Runs the operation through C-extensions from cython.
            * ``'numba'`` : Runs the operation through JIT compiled code from numba.
            * ``None`` : Defaults to ``'cython'`` or globally setting
              ``compute.use_numba``

            .. versionadded:: 1.4.0

        engine_kwargs : dict, default None
            * For ``'cython'`` engine, there are no accepted ``engine_kwargs``
            * For ``'numba'`` engine, the engine can accept ``nopython``, ``nogil``
              and ``parallel`` dictionary keys. The values must either be ``True`` or
              ``False``. The default ``engine_kwargs`` for the ``'numba'`` engine is
              ``{{'nopython': True, 'nogil': False, 'parallel': False}}``

            .. versionadded:: 1.4.0

        Returns
        -------
        pandas.Series or pandas.DataFrame
        %(see_also)s
        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],
        ...                    'B': [np.nan, 2, 3, 4, 5],
        ...                    'C': [1, 2, 1, 1, 2]}, columns=['A', 'B', 'C'])

        Groupby one column and return the mean of the remaining columns in
        each group.

        >>> df.groupby('A').mean()
             B         C
        A
        1  3.0  1.333333
        2  4.0  1.500000

        Groupby two columns and return the mean of the remaining column.

        >>> df.groupby(['A', 'B']).mean()
                 C
        A B
        1 2.0  2.0
          4.0  1.0
        2 3.0  1.0
          5.0  2.0

        Groupby one column and return the mean of only particular column in
        the group.

        >>> df.groupby('A')['B'].mean()
        A
        1    3.0
        2    4.0
        Name: B, dtype: float64
        """
        numeric_only_bool = self._resolve_numeric_only(numeric_only)

        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import sliding_mean

            return self._numba_agg_general(sliding_mean, engine_kwargs, "groupby_mean")
        else:
            result = self._cython_agg_general(
                "mean",
                alt=lambda x: Series(x).mean(numeric_only=numeric_only_bool),
                numeric_only=numeric_only_bool,
            )
            return result.__finalize__(self.obj, method="groupby")

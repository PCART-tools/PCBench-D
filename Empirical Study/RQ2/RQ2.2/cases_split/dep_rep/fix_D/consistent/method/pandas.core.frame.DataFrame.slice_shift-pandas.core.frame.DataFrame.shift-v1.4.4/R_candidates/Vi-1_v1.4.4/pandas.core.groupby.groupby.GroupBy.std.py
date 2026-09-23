    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def std(
        self,
        ddof: int = 1,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
    ):
        """
        Compute standard deviation of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

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
        Series or DataFrame
            Standard deviation of values within each group.
        """
        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import sliding_var

            return np.sqrt(
                self._numba_agg_general(sliding_var, engine_kwargs, "groupby_std", ddof)
            )
        else:
            return self._get_cythonized_result(
                libgroupby.group_var,
                needs_counts=True,
                cython_dtype=np.dtype(np.float64),
                post_processing=lambda vals, inference: np.sqrt(vals),
                ddof=ddof,
            )

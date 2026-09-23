    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def std(
        self,
        ddof: int = 1,
        engine: str | None = None,
        engine_kwargs: dict[str, bool] | None = None,
        numeric_only: bool | lib.NoDefault = lib.no_default,
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

        numeric_only : bool, default True
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

        Returns
        -------
        Series or DataFrame
            Standard deviation of values within each group.
        """
        if maybe_use_numba(engine):
            from pandas.core._numba.kernels import sliding_var

            return np.sqrt(self._numba_agg_general(sliding_var, engine_kwargs, ddof))
        else:
            # Resolve numeric_only so that var doesn't warn
            numeric_only_bool = self._resolve_numeric_only("std", numeric_only, axis=0)
            if (
                numeric_only_bool
                and self.obj.ndim == 1
                and not is_numeric_dtype(self.obj.dtype)
            ):
                raise TypeError(
                    f"{type(self).__name__}.std called with "
                    f"numeric_only={numeric_only} and dtype {self.obj.dtype}"
                )
            result = self._get_cythonized_result(
                libgroupby.group_var,
                cython_dtype=np.dtype(np.float64),
                numeric_only=numeric_only_bool,
                needs_counts=True,
                post_processing=lambda vals, inference: np.sqrt(vals),
                ddof=ddof,
            )
            self._maybe_warn_numeric_only_depr("std", result, numeric_only)
            return result

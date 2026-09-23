    def applymap(
        self, func: PythonFuncType, na_action: str | None = None, **kwargs
    ) -> DataFrame:
        """
        Apply a function to a Dataframe elementwise.

        This method applies a function that accepts and returns a scalar
        to every element of a DataFrame.

        Parameters
        ----------
        func : callable
            Python function, returns a single value from a single value.
        na_action : {None, 'ignore'}, default None
            If ‘ignore’, propagate NaN values, without passing them to func.

            .. versionadded:: 1.2

        **kwargs
            Additional keyword arguments to pass as keywords arguments to
            `func`.

            .. versionadded:: 1.3.0

        Returns
        -------
        DataFrame
            Transformed DataFrame.

        See Also
        --------
        DataFrame.apply : Apply a function along input axis of DataFrame.

        Examples
        --------
        >>> df = pd.DataFrame([[1, 2.12], [3.356, 4.567]])
        >>> df
               0      1
        0  1.000  2.120
        1  3.356  4.567

        >>> df.applymap(lambda x: len(str(x)))
           0  1
        0  3  4
        1  5  5

        Like Series.map, NA values can be ignored:

        >>> df_copy = df.copy()
        >>> df_copy.iloc[0, 0] = pd.NA
        >>> df_copy.applymap(lambda x: len(str(x)), na_action='ignore')
             0  1
        0  NaN  4
        1  5.0  5

        Note that a vectorized version of `func` often exists, which will
        be much faster. You could square each number elementwise.

        >>> df.applymap(lambda x: x**2)
                   0          1
        0   1.000000   4.494400
        1  11.262736  20.857489

        But it's better to avoid applymap in that case.

        >>> df ** 2
                   0          1
        0   1.000000   4.494400
        1  11.262736  20.857489
        """
        if na_action not in {"ignore", None}:
            raise ValueError(
                f"na_action must be 'ignore' or None. Got {repr(na_action)}"
            )
        ignore_na = na_action == "ignore"
        func = functools.partial(func, **kwargs)

        # if we have a dtype == 'M8[ns]', provide boxed values
        def infer(x):
            if x.empty:
                return lib.map_infer(x, func, ignore_na=ignore_na)
            return lib.map_infer(x.astype(object)._values, func, ignore_na=ignore_na)

        return self.apply(infer).__finalize__(self, "applymap")

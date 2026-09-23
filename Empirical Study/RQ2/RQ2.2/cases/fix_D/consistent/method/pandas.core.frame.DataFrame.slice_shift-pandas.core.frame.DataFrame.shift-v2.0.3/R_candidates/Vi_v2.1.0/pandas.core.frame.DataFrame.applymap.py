    def applymap(
        self, func: PythonFuncType, na_action: NaAction | None = None, **kwargs
    ) -> DataFrame:
        """
        Apply a function to a Dataframe elementwise.

        .. deprecated:: 2.1.0

           DataFrame.applymap has been deprecated. Use DataFrame.map instead.

        This method applies a function that accepts and returns a scalar
        to every element of a DataFrame.

        Parameters
        ----------
        func : callable
            Python function, returns a single value from a single value.
        na_action : {None, 'ignore'}, default None
            If 'ignore', propagate NaN values, without passing them to func.
        **kwargs
            Additional keyword arguments to pass as keywords arguments to
            `func`.

        Returns
        -------
        DataFrame
            Transformed DataFrame.

        See Also
        --------
        DataFrame.apply : Apply a function along input axis of DataFrame.
        DataFrame.map : Apply a function along input axis of DataFrame.
        DataFrame.replace: Replace values given in `to_replace` with `value`.

        Examples
        --------
        >>> df = pd.DataFrame([[1, 2.12], [3.356, 4.567]])
        >>> df
               0      1
        0  1.000  2.120
        1  3.356  4.567

        >>> df.map(lambda x: len(str(x)))
           0  1
        0  3  4
        1  5  5
        """
        warnings.warn(
            "DataFrame.applymap has been deprecated. Use DataFrame.map instead.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        return self.map(func, na_action=na_action, **kwargs)

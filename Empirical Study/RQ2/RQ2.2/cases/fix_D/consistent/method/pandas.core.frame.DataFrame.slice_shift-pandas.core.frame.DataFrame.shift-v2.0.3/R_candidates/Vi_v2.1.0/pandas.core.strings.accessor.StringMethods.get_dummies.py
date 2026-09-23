    @forbid_nonstring_types(["bytes"])
    def get_dummies(self, sep: str = "|"):
        """
        Return DataFrame of dummy/indicator variables for Series.

        Each string in Series is split by sep and returned as a DataFrame
        of dummy/indicator variables.

        Parameters
        ----------
        sep : str, default "|"
            String to split on.

        Returns
        -------
        DataFrame
            Dummy variables corresponding to values of the Series.

        See Also
        --------
        get_dummies : Convert categorical variable into dummy/indicator
            variables.

        Examples
        --------
        >>> pd.Series(['a|b', 'a', 'a|c']).str.get_dummies()
           a  b  c
        0  1  1  0
        1  1  0  0
        2  1  0  1

        >>> pd.Series(['a|b', np.nan, 'a|c']).str.get_dummies()
           a  b  c
        0  1  1  0
        1  0  0  0
        2  1  0  1
        """
        # we need to cast to Series of strings as only that has all
        # methods available for making the dummies...
        result, name = self._data.array._str_get_dummies(sep)
        return self._wrap_result(
            result,
            name=name,
            expand=True,
            returns_string=False,
        )

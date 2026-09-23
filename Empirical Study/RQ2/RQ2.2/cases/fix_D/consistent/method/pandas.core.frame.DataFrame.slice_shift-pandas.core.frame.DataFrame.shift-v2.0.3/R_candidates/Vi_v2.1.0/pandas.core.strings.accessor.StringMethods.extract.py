    @forbid_nonstring_types(["bytes"])
    def extract(
        self, pat: str, flags: int = 0, expand: bool = True
    ) -> DataFrame | Series | Index:
        r"""
        Extract capture groups in the regex `pat` as columns in a DataFrame.

        For each subject string in the Series, extract groups from the
        first match of regular expression `pat`.

        Parameters
        ----------
        pat : str
            Regular expression pattern with capturing groups.
        flags : int, default 0 (no flags)
            Flags from the ``re`` module, e.g. ``re.IGNORECASE``, that
            modify regular expression matching for things like case,
            spaces, etc. For more details, see :mod:`re`.
        expand : bool, default True
            If True, return DataFrame with one column per capture group.
            If False, return a Series/Index if there is one capture group
            or DataFrame if there are multiple capture groups.

        Returns
        -------
        DataFrame or Series or Index
            A DataFrame with one row for each subject string, and one
            column for each group. Any capture group names in regular
            expression pat will be used for column names; otherwise
            capture group numbers will be used. The dtype of each result
            column is always object, even when no match is found. If
            ``expand=False`` and pat has only one capture group, then
            return a Series (if subject is a Series) or Index (if subject
            is an Index).

        See Also
        --------
        extractall : Returns all matches (not just the first match).

        Examples
        --------
        A pattern with two groups will return a DataFrame with two columns.
        Non-matches will be NaN.

        >>> s = pd.Series(['a1', 'b2', 'c3'])
        >>> s.str.extract(r'([ab])(\d)')
            0    1
        0    a    1
        1    b    2
        2  NaN  NaN

        A pattern may contain optional groups.

        >>> s.str.extract(r'([ab])?(\d)')
            0  1
        0    a  1
        1    b  2
        2  NaN  3

        Named groups will become column names in the result.

        >>> s.str.extract(r'(?P<letter>[ab])(?P<digit>\d)')
        letter digit
        0      a     1
        1      b     2
        2    NaN   NaN

        A pattern with one group will return a DataFrame with one column
        if expand=True.

        >>> s.str.extract(r'[ab](\d)', expand=True)
            0
        0    1
        1    2
        2  NaN

        A pattern with one group will return a Series if expand=False.

        >>> s.str.extract(r'[ab](\d)', expand=False)
        0      1
        1      2
        2    NaN
        dtype: object
        """
        from pandas import DataFrame

        if not isinstance(expand, bool):
            raise ValueError("expand must be True or False")

        regex = re.compile(pat, flags=flags)
        if regex.groups == 0:
            raise ValueError("pattern contains no capture groups")

        if not expand and regex.groups > 1 and isinstance(self._data, ABCIndex):
            raise ValueError("only one regex group is supported with Index")

        obj = self._data
        result_dtype = _result_dtype(obj)

        returns_df = regex.groups > 1 or expand

        if returns_df:
            name = None
            columns = _get_group_names(regex)

            if obj.array.size == 0:
                result = DataFrame(columns=columns, dtype=result_dtype)

            else:
                result_list = self._data.array._str_extract(
                    pat, flags=flags, expand=returns_df
                )

                result_index: Index | None
                if isinstance(obj, ABCSeries):
                    result_index = obj.index
                else:
                    result_index = None

                result = DataFrame(
                    result_list, columns=columns, index=result_index, dtype=result_dtype
                )

        else:
            name = _get_single_group_name(regex)
            result = self._data.array._str_extract(pat, flags=flags, expand=returns_df)
        return self._wrap_result(result, name=name)

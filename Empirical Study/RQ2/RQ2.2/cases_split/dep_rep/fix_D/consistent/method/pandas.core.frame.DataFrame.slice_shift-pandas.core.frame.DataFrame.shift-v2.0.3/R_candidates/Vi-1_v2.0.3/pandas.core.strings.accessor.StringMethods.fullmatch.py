    @forbid_nonstring_types(["bytes"])
    def fullmatch(self, pat, case: bool = True, flags: int = 0, na=None):
        """
        Determine if each string entirely matches a regular expression.

        .. versionadded:: 1.1.0

        Parameters
        ----------
        pat : str
            Character sequence or regular expression.
        case : bool, default True
            If True, case sensitive.
        flags : int, default 0 (no flags)
            Regex module flags, e.g. re.IGNORECASE.
        na : scalar, optional
            Fill value for missing values. The default depends on dtype of the
            array. For object-dtype, ``numpy.nan`` is used. For ``StringDtype``,
            ``pandas.NA`` is used.

        Returns
        -------
        Series/Index/array of boolean values

        See Also
        --------
        match : Similar, but also returns `True` when only a *prefix* of the string
            matches the regular expression.
        extract : Extract matched groups.
        """
        result = self._data.array._str_fullmatch(pat, case=case, flags=flags, na=na)
        return self._wrap_result(result, fill_value=na, returns_string=False)

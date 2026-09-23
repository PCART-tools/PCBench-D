    @forbid_nonstring_types(["bytes"])
    def encode(self, encoding, errors: str = "strict"):
        """
        Encode character string in the Series/Index using indicated encoding.

        Equivalent to :meth:`str.encode`.

        Parameters
        ----------
        encoding : str
        errors : str, optional

        Returns
        -------
        Series/Index of objects

        Examples
        --------
        >>> ser = pd.Series(['cow', '123', '()'])
        >>> ser.str.encode(encoding='ascii')
        0     b'cow'
        1     b'123'
        2      b'()'
        dtype: object
        """
        result = self._data.array._str_encode(encoding, errors)
        return self._wrap_result(result, returns_string=False)

    def decode(self, encoding, errors: str = "strict"):
        """
        Decode character string in the Series/Index using indicated encoding.

        Equivalent to :meth:`str.decode` in python2 and :meth:`bytes.decode` in
        python3.

        Parameters
        ----------
        encoding : str
        errors : str, optional

        Returns
        -------
        Series or Index

        Examples
        --------
        For Series:

        >>> ser = pd.Series([b'cow', b'123', b'()'])
        >>> ser.str.decode('ascii')
        0   cow
        1   123
        2   ()
        dtype: object
        """
        # TODO: Add a similar _bytes interface.
        if encoding in _cpython_optimized_decoders:
            # CPython optimized implementation
            f = lambda x: x.decode(encoding, errors)
        else:
            decoder = codecs.getdecoder(encoding)
            f = lambda x: decoder(x, errors)[0]
        arr = self._data.array
        # assert isinstance(arr, (StringArray,))
        result = arr._str_map(f)
        return self._wrap_result(result)

    def decode(self, encoding: TransferEncoding, *, strict: bool = True) -> Series:
        r"""
        Decode values using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.
        strict
            Raise an error if the underlying value cannot be decoded,
            otherwise mask out with a null value.

        Returns
        -------
        Series
            Series of data type :class:`Binary`.

        Examples
        --------
        >>> s = pl.Series("color", ["000000", "ffff00", "0000ff"])
        >>> s.str.decode("hex")
        shape: (3,)
        Series: 'color' [binary]
        [
                b"\x00\x00\x00"
                b"\xff\xff\x00"
                b"\x00\x00\xff"
        ]
        """

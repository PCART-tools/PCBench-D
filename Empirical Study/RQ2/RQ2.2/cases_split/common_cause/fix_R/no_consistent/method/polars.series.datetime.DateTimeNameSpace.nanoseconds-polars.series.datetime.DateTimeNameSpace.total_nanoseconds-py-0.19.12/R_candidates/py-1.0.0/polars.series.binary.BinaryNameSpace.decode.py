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
            Series of data type :class:`String`.

        Examples
        --------
        Decode values using hexadecimal encoding.

        >>> s = pl.Series("colors", [b"000000", b"ffff00", b"0000ff"])
        >>> s.bin.decode("hex")
        shape: (3,)
        Series: 'colors' [binary]
        [
            b"\x00\x00\x00"
            b"\xff\xff\x00"
            b"\x00\x00\xff"
        ]

        Decode values using Base64 encoding.

        >>> s = pl.Series("colors", [b"AAAA", b"//8A", b"AAD/"])
        >>> s.bin.decode("base64")
        shape: (3,)
        Series: 'colors' [binary]
        [
            b"\x00\x00\x00"
            b"\xff\xff\x00"
            b"\x00\x00\xff"
        ]

        Set `strict=False` to set invalid values to null instead of raising an error.

        >>> s = pl.Series("colors", [b"000000", b"ffff00", b"invalid_value"])
        >>> s.bin.decode("hex", strict=False)
        shape: (3,)
        Series: 'colors' [binary]
        [
            b"\x00\x00\x00"
            b"\xff\xff\x00"
            null
        ]
        """

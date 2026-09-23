    def encode(self, encoding: TransferEncoding) -> Series:
        r"""
        Encode values using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.

        Returns
        -------
        Series
            Series of data type :class:`String`.

        Examples
        --------
        Encode values using hexadecimal encoding.

        >>> s = pl.Series("colors", [b"\x00\x00\x00", b"\xff\xff\x00", b"\x00\x00\xff"])
        >>> s.bin.encode("hex")
        shape: (3,)
        Series: 'colors' [str]
        [
            "000000"
            "ffff00"
            "0000ff"
        ]

        Encode values using Base64 encoding.

        >>> s.bin.encode("base64")
        shape: (3,)
        Series: 'colors' [str]
        [
            "AAAA"
            "//8A"
            "AAD/"
        ]
        """

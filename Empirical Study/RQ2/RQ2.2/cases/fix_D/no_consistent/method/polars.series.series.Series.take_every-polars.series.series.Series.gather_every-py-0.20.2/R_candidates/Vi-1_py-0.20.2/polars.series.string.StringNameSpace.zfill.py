    @deprecate_renamed_parameter("alignment", "length", version="0.19.12")
    def zfill(self, length: int) -> Series:
        """
        Pad the start of the string with zeros until it reaches the given length.

        A sign prefix (`-`) is handled by inserting the padding after the sign
        character rather than before.

        Parameters
        ----------
        length
            Pad the string until it reaches this length. Strings with length equal to
            or greater than this value are returned as-is.

        See Also
        --------
        pad_start

        Notes
        -----
        This method is intended for padding numeric strings. If your data contains
        non-ASCII characters, use :func:`pad_start` instead.

        Examples
        --------
        >>> s = pl.Series([-1, 123, 999999, None])
        >>> s.cast(pl.Utf8).str.zfill(4)
        shape: (4,)
        Series: '' [str]
        [
                "-001"
                "0123"
                "999999"
                null
        ]

        """

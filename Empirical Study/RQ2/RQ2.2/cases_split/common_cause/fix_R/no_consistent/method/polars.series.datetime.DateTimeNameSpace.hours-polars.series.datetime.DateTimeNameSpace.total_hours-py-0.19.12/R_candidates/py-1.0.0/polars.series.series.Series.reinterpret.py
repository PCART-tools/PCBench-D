    def reinterpret(self, *, signed: bool = True) -> Series:
        """
        Reinterpret the underlying bits as a signed/unsigned integer.

        This operation is only allowed for 64bit integers. For lower bits integers,
        you can safely use that cast operation.

        Parameters
        ----------
        signed
            If True, reinterpret as `pl.Int64`. Otherwise, reinterpret as `pl.UInt64`.

        Examples
        --------
        >>> s = pl.Series("a", [-(2**60), -2, 3])
        >>> s
        shape: (3,)
        Series: 'a' [i64]
        [
                -1152921504606846976
                -2
                3
        ]
        >>> s.reinterpret(signed=False)
        shape: (3,)
        Series: 'a' [u64]
        [
                17293822569102704640
                18446744073709551614
                3
        ]
        """

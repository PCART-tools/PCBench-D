    def gather(
        self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
    ) -> Series:
        """
        Take values by index.

        Parameters
        ----------
        indices
            Index location used for selection.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4])
        >>> s.gather([1, 3])
        shape: (2,)
        Series: 'a' [i64]
        [
                2
                4
        ]

        """

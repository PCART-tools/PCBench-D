    def std(
        self,
        axis=None,
        dtype=None,
        out=None,
        ddof: int = 1,
        keepdims: bool = False,
        skipna: bool = True,
    ):
        """
        Return sample standard deviation over requested axis.

        Normalized by N-1 by default. This can be changed using the ddof argument

        Parameters
        ----------
        axis : int optional, default None
            Axis for the function to be applied on.
        ddof : int, default 1
            Degrees of Freedom. The divisor used in calculations is N - ddof,
            where N represents the number of elements.
        skipna : bool, default True
            Exclude NA/null values. If an entire row/column is NA, the result will be
            NA.

        Returns
        -------
        Timedelta
        """
        # Because std is translation-invariant, we can get self.std
        #  by calculating (self - Timestamp(0)).std, and we can do it
        #  without creating a copy by using a view on self._ndarray
        from pandas.core.arrays import TimedeltaArray

        tda = TimedeltaArray(self._ndarray.view("i8"))
        return tda.std(
            axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims, skipna=skipna
        )

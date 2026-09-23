    def nsmallest(self, n=5, keep='first'):
        """
        Return the smallest `n` elements.

        Parameters
        ----------
        n : int
            Return this many ascending sorted values
        keep : {'first', 'last', False}, default 'first'
            Where there are duplicate values:
            - ``first`` : take the first occurrence.
            - ``last`` : take the last occurrence.

        Returns
        -------
        bottom_n : Series
            The n smallest values in the Series, in sorted order

        Notes
        -----
        Faster than ``.sort_values().head(n)`` for small `n` relative to
        the size of the ``Series`` object.

        See Also
        --------
        Series.nlargest

        Examples
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> s = pd.Series(np.random.randn(10**6))
        >>> s.nsmallest(10)  # only sorts up to the N requested
        288532   -4.954580
        732345   -4.835960
        64803    -4.812550
        446457   -4.609998
        501225   -4.483945
        669476   -4.472935
        973615   -4.401699
        621279   -4.355126
        773916   -4.347355
        359919   -4.331927
        dtype: float64
        """
        return algorithms.SelectNSeries(self, n=n, keep=keep).nsmallest()

    def nlargest(self, n=5, keep='first'):
        """Return the largest `n` elements.

        Parameters
        ----------
        n : int
            Return this many descending sorted values
        keep : {'first', 'last', False}, default 'first'
            Where there are duplicate values:
            - ``first`` : take the first occurrence.
            - ``last`` : take the last occurrence.

        Returns
        -------
        top_n : Series
            The n largest values in the Series, in sorted order

        Notes
        -----
        Faster than ``.sort_values(ascending=False).head(n)`` for small `n`
        relative to the size of the ``Series`` object.

        See Also
        --------
        Series.nsmallest

        Examples
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> s = pd.Series(np.random.randn(10**6))
        >>> s.nlargest(10)  # only sorts up to the N requested
        219921    4.644710
        82124     4.608745
        421689    4.564644
        425277    4.447014
        718691    4.414137
        43154     4.403520
        283187    4.313922
        595519    4.273635
        503969    4.250236
        121637    4.240952
        dtype: float64
        """
        return algorithms.SelectNSeries(self, n=n, keep=keep).nlargest()

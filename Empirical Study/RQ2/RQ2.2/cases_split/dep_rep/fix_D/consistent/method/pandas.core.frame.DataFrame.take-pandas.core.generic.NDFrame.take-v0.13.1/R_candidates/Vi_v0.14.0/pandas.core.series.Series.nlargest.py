    def nlargest(self, n=5, take_last=False):
        """Return the largest `n` elements.

        Parameters
        ----------
        n : int
            Return this many descending sorted values
        take_last : bool
            Where there are duplicate values, take the last duplicate

        Returns
        -------
        top_n : Series
            The n largest values in the Series, in sorted order

        Notes
        -----
        Faster than ``.order(ascending=False).head(n)`` for small `n` relative
        to the size of the ``Series`` object.

        See Also
        --------
        Series.nsmallest

        Examples
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> s = pd.Series(np.random.randn(1e6))
        >>> s.nlargest(10)  # only sorts up to the N requested
        """
        return select_n(self, n=n, take_last=take_last, method='nlargest')

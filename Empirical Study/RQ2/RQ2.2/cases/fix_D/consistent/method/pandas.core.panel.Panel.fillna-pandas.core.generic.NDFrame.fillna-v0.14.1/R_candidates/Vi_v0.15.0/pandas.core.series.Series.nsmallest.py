    def nsmallest(self, n=5, take_last=False):
        """Return the smallest `n` elements.

        Parameters
        ----------
        n : int
            Return this many ascending sorted values
        take_last : bool
            Where there are duplicate values, take the last duplicate

        Returns
        -------
        bottom_n : Series
            The n smallest values in the Series, in sorted order

        Notes
        -----
        Faster than ``.order().head(n)`` for small `n` relative to
        the size of the ``Series`` object.

        See Also
        --------
        Series.nlargest

        Examples
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> s = pd.Series(np.random.randn(1e6))
        >>> s.nsmallest(10)  # only sorts up to the N requested
        """
        return select_n(self, n=n, take_last=take_last, method='nsmallest')

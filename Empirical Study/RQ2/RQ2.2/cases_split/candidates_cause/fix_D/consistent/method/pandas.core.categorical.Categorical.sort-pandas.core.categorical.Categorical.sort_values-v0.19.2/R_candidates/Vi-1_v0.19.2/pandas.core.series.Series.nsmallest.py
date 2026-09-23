    @deprecate_kwarg('take_last', 'keep', mapping={True: 'last',
                                                   False: 'first'})
    def nsmallest(self, n=5, keep='first'):
        """Return the smallest `n` elements.

        Parameters
        ----------
        n : int
            Return this many ascending sorted values
        keep : {'first', 'last', False}, default 'first'
            Where there are duplicate values:
            - ``first`` : take the first occurrence.
            - ``last`` : take the last occurrence.
        take_last : deprecated

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
        >>> s = pd.Series(np.random.randn(1e6))
        >>> s.nsmallest(10)  # only sorts up to the N requested
        """
        return algos.select_n_series(self, n=n, keep=keep, method='nsmallest')

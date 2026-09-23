    def describe(self, percentile_width=50):
        """
        Generate various summary statistics of Series, excluding NaN
        values. These include: count, mean, std, min, max, and
        lower%/50%/upper% percentiles

        Parameters
        ----------
        percentile_width : float, optional
            width of the desired uncertainty interval, default is 50,
            which corresponds to lower=25, upper=75

        Returns
        -------
        desc : Series
        """
        try:
            from collections import Counter
        except ImportError:  # pragma: no cover
            # For Python < 2.7, we include a local copy of this:
            from pandas.util.counter import Counter

        if self.dtype == object:
            names = ['count', 'unique']
            objcounts = Counter(self.dropna().values)
            data = [self.count(), len(objcounts)]
            if data[1] > 0:
                names += ['top', 'freq']
                top, freq = objcounts.most_common(1)[0]
                data += [top, freq]

        elif issubclass(self.dtype.type, np.datetime64):
            names = ['count', 'unique']
            asint = self.dropna().values.view('i8')
            objcounts = Counter(asint)
            data = [self.count(), len(objcounts)]
            if data[1] > 0:
                top, freq = objcounts.most_common(1)[0]
                names += ['first', 'last', 'top', 'freq']
                data += [lib.Timestamp(asint.min()),
                         lib.Timestamp(asint.max()),
                         lib.Timestamp(top), freq]
        else:

            lb = .5 * (1. - percentile_width / 100.)
            ub = 1. - lb

            def pretty_name(x):
                x *= 100
                if x == int(x):
                    return '%.0f%%' % x
                else:
                    return '%.1f%%' % x

            names = ['count']
            data = [self.count()]
            names += ['mean', 'std', 'min', pretty_name(lb), '50%',
                      pretty_name(ub), 'max']
            data += [self.mean(), self.std(), self.min(),
                     self.quantile(
                         lb), self.median(), self.quantile(ub),
                     self.max()]

        return self._constructor(data, index=names).__finalize__(self)

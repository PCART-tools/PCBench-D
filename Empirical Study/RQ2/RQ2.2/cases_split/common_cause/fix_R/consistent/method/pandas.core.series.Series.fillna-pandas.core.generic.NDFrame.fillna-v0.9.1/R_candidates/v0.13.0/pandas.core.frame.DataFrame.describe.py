    def describe(self, percentile_width=50):
        """
        Generate various summary statistics of each column, excluding
        NaN values. These include: count, mean, std, min, max, and
        lower%/50%/upper% percentiles

        Parameters
        ----------
        percentile_width : float, optional
            width of the desired uncertainty interval, default is 50,
            which corresponds to lower=25, upper=75

        Returns
        -------
        DataFrame of summary statistics
        """
        numdata = self._get_numeric_data()

        if len(numdata.columns) == 0:
            return DataFrame(dict((k, v.describe())
                                  for k, v in compat.iteritems(self)),
                             columns=self.columns)

        lb = .5 * (1. - percentile_width / 100.)
        ub = 1. - lb

        def pretty_name(x):
            x *= 100
            if x == int(x):
                return '%.0f%%' % x
            else:
                return '%.1f%%' % x

        destat_columns = ['count', 'mean', 'std', 'min',
                          pretty_name(lb), '50%', pretty_name(ub),
                          'max']

        destat = []

        for i in range(len(numdata.columns)):
            series = numdata.iloc[:, i]
            destat.append([series.count(), series.mean(), series.std(),
                           series.min(), series.quantile(lb), series.median(),
                           series.quantile(ub), series.max()])

        return self._constructor(lmap(list, zip(*destat)),
                                 index=destat_columns, columns=numdata.columns)

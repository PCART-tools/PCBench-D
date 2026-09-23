    def _get_values(self, indexer):
        try:
            return self._constructor(
                self._data.get_slice(indexer), fastpath=True
            ).__finalize__(self)
        except ValueError:
            # mpl compat if we look up e.g. ser[:, np.newaxis];
            #  see tests.series.timeseries.test_mpl_compat_hack
            return self._values[indexer]

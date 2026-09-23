    def _get_values(self, indexer):
        try:
            new_mgr = self._mgr.getitem_mgr(indexer)
            return self._constructor(new_mgr).__finalize__(self)
        except ValueError:
            # mpl compat if we look up e.g. ser[:, np.newaxis];
            #  see tests.series.timeseries.test_mpl_compat_hack
            # the asarray is needed to avoid returning a 2D DatetimeArray
            return np.asarray(self._values[indexer])

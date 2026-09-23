    def _get_values_tuple(self, key: tuple):
        # mpl hackaround
        if com.any_none(*key):
            # mpl compat if we look up e.g. ser[:, np.newaxis];
            #  see tests.series.timeseries.test_mpl_compat_hack
            # the asarray is needed to avoid returning a 2D DatetimeArray
            result = np.asarray(self._values[key])
            disallow_ndim_indexing(result)
            return result

        if not isinstance(self.index, MultiIndex):
            raise KeyError("key of type tuple not found and not a MultiIndex")

        # If key is contained, would have returned by now
        indexer, new_index = self.index.get_loc_level(key)
        new_ser = self._constructor(self._values[indexer], index=new_index, copy=False)
        if using_copy_on_write() and isinstance(indexer, slice):
            new_ser._mgr.add_references(self._mgr)  # type: ignore[arg-type]
        return new_ser.__finalize__(self)

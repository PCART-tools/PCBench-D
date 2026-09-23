    def _multi_take_opportunity(self, tup):
        from pandas.core.generic import NDFrame

        # ugly hack for GH #836
        if not isinstance(self.obj, NDFrame):
            return False

        if not all(is_list_like_indexer(x) for x in tup):
            return False

        # just too complicated
        for indexer, ax in zip(tup, self.obj._data.axes):
            if isinstance(ax, MultiIndex):
                return False
            elif com.is_bool_indexer(indexer):
                return False
            elif not ax.is_unique:
                return False

        return True

    def _multi_take_opportunity(self, tup):
        from pandas.core.generic import NDFrame

        # ugly hack for GH #836
        if not isinstance(self.obj, NDFrame):
            return False

        if not all(_is_list_like(x) for x in tup):
            return False

        # just too complicated
        for indexer, ax in zip(tup, self.obj._data.axes):
            if isinstance(ax, MultiIndex):
                return False
            elif com._is_bool_indexer(indexer):
                return False

        return True

    def _is_nested_tuple_indexer(self, tup):
        if any([isinstance(ax, MultiIndex) for ax in self.obj.axes]):
            return any([is_nested_tuple(tup, ax) for ax in self.obj.axes])
        return False

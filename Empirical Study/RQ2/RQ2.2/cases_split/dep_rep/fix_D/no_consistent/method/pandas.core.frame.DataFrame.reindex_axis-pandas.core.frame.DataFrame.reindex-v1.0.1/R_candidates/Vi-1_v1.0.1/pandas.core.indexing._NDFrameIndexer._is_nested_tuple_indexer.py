    def _is_nested_tuple_indexer(self, tup: Tuple) -> bool:
        """
        Returns
        -------
        bool
        """
        if any(isinstance(ax, ABCMultiIndex) for ax in self.obj.axes):
            return any(is_nested_tuple(tup, ax) for ax in self.obj.axes)
        return False

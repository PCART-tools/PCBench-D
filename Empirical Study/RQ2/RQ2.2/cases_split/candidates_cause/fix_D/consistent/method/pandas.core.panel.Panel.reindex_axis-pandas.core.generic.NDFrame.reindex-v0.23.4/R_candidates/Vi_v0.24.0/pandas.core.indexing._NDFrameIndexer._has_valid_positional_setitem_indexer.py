    def _has_valid_positional_setitem_indexer(self, indexer):
        """ validate that an positional indexer cannot enlarge its target
        will raise if needed, does not modify the indexer externally
        """
        if isinstance(indexer, dict):
            raise IndexError("{0} cannot enlarge its target object"
                             .format(self.name))
        else:
            if not isinstance(indexer, tuple):
                indexer = self._tuplify(indexer)
            for ax, i in zip(self.obj.axes, indexer):
                if isinstance(i, slice):
                    # should check the stop slice?
                    pass
                elif is_list_like_indexer(i):
                    # should check the elements?
                    pass
                elif is_integer(i):
                    if i >= len(ax):
                        raise IndexError("{name} cannot enlarge its target "
                                         "object".format(name=self.name))
                elif isinstance(i, dict):
                    raise IndexError("{name} cannot enlarge its target object"
                                     .format(name=self.name))

        return True

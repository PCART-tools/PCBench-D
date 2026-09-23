    @final
    def __setitem__(self, key, value) -> None:
        if not PYPY and using_copy_on_write():
            if sys.getrefcount(self.obj) <= 2:
                warnings.warn(
                    _chained_assignment_msg, ChainedAssignmentError, stacklevel=2
                )

        check_dict_or_set_indexers(key)
        if isinstance(key, tuple):
            key = tuple(list(x) if is_iterator(x) else x for x in key)
            key = tuple(com.apply_if_callable(x, self.obj) for x in key)
        else:
            key = com.apply_if_callable(key, self.obj)
        indexer = self._get_setitem_indexer(key)
        self._has_valid_setitem_indexer(key)

        iloc = self if self.name == "iloc" else self.obj.iloc
        iloc._setitem_with_indexer(indexer, value, self.name)

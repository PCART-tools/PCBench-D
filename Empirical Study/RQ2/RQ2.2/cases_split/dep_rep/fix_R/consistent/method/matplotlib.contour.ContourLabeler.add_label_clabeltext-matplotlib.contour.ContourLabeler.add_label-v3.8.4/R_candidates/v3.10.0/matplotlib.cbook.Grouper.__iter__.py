    def __iter__(self):
        """
        Iterate over each of the disjoint sets as a list.

        The iterator is invalid if interleaved with calls to join().
        """
        unique_groups = {id(group): group for group in self._mapping.values()}
        for group in unique_groups.values():
            yield sorted(group, key=self._ordering.__getitem__)

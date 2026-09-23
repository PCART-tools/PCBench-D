    def _wrap_joined_index(self, joined, other):
        names = self.names if self.names == other.names else None
        return MultiIndex.from_tuples(joined, names=names)

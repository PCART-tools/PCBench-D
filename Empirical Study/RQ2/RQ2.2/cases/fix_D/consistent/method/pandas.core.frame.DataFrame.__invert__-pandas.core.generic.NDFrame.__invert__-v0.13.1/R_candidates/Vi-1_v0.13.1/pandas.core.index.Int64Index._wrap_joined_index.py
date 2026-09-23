    def _wrap_joined_index(self, joined, other):
        name = self.name if self.name == other.name else None
        return Int64Index(joined, name=name)

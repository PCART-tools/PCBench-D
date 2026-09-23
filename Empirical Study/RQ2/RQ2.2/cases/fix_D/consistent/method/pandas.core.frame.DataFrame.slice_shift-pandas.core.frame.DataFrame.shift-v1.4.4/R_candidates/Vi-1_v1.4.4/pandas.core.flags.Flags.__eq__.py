    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.allows_duplicate_labels == other.allows_duplicate_labels
        return False

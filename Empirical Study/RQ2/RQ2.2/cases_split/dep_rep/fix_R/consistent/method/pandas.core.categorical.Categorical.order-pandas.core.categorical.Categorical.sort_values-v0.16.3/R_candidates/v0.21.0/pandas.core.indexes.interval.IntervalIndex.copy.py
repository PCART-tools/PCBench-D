    @Appender(_index_shared_docs['copy'])
    def copy(self, deep=False, name=None):
        left = self.left.copy(deep=True) if deep else self.left
        right = self.right.copy(deep=True) if deep else self.right
        name = name if name is not None else self.name
        return type(self).from_arrays(left, right, name=name)

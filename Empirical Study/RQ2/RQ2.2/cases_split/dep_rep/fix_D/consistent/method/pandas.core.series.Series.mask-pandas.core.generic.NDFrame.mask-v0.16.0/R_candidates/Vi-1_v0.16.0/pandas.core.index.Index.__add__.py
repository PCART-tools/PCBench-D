    def __add__(self, other):
        if isinstance(other, Index):
            warnings.warn("using '+' to provide set union with Indexes is deprecated, "
                          "use '|' or .union()",FutureWarning)
            return self.union(other)
        return Index(np.array(self) + other)

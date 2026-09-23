    def __add__(self, other):
        if com.is_list_like(other):
            warnings.warn("using '+' to provide set union with Indexes is deprecated, "
                          "use '|' or .union()", FutureWarning)
        if isinstance(other, Index):
            return self.union(other)
        return Index(np.array(self) + other)

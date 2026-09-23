    def __radd__(self, other):
        if com.is_list_like(other):
            warnings.warn("using '+' to provide set union with Indexes is deprecated, "
                          "use '|' or .union()", FutureWarning)
        return Index(other + np.array(self))

    def __sub__(self, other):
        if isinstance(other, Index):
            warnings.warn("using '-' to provide set differences with Indexes is deprecated, "
                          "use .difference()",FutureWarning)
        return self.difference(other)

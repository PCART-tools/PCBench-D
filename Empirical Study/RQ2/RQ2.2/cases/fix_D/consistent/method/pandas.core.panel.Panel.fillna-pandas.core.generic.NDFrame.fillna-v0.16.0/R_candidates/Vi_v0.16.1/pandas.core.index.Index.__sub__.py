    def __sub__(self, other):
        warnings.warn("using '-' to provide set differences with Indexes is deprecated, "
                      "use .difference()",FutureWarning)
        return self.difference(other)

    def __iter__(self):
        warnings.warn(
            "Columnar iteration over characters will be deprecated in future releases.",
            FutureWarning,
            stacklevel=2,
        )
        i = 0
        g = self.get(i)
        while g.notna().any():
            yield g
            i += 1
            g = self.get(i)

    def __iter__(self):
        warnings.warn(
            "Columnar iteration over characters will be deprecated in future releases.",
            FutureWarning,
            stacklevel=find_stack_level(),
        )
        i = 0
        g = self.get(i)
        while g.notna().any():
            yield g
            i += 1
            g = self.get(i)

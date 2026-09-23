    def diff(self, n: int) -> Self:
        # only reached with self.ndim == 2
        return self.apply("diff", n=n)

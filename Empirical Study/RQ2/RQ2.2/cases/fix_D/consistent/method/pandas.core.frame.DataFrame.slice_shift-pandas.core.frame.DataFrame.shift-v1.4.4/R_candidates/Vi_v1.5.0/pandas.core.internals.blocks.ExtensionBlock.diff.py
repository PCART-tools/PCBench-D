    def diff(self, n: int, axis: int = 1) -> list[Block]:
        if axis == 0 and n != 0:
            # n==0 case will be a no-op so let is fall through
            # Since we only have one column, the result will be all-NA.
            #  Create this result by shifting along axis=0 past the length of
            #  our values.
            return super().diff(len(self.values), axis=0)
        if axis == 1:
            # TODO(EA2D): unnecessary with 2D EAs
            # we are by definition 1D.
            axis = 0
        return super().diff(n, axis)

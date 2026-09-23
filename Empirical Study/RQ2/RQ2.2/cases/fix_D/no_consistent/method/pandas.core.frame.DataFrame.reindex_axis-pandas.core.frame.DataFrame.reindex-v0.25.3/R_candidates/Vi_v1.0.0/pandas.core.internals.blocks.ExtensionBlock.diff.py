    def diff(self, n: int, axis: int = 1) -> List["Block"]:
        if axis == 1:
            # we are by definition 1D.
            axis = 0
        return super().diff(n, axis)

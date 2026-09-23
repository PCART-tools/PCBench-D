    def diff(self: T, n: int, axis: int) -> T:
        if axis == 1:
            # DataFrame only calls this for n=0, in which case performing it
            # with axis=0 is equivalent
            assert n == 0
            axis = 0
        return self.apply(algos.diff, n=n, axis=axis)

    def diff(self, n: int, axis: AxisInt = 1) -> list[Block]:
        """return block for the diff of the values"""
        # only reached with ndim == 2 and axis == 1
        new_values = algos.diff(self.values, n, axis=axis)
        return [self.make_block(values=new_values)]

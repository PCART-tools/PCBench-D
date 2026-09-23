    def diff(self, n: int, axis: AxisInt = 1) -> list[Block]:
        # only reached with ndim == 2 and axis == 1
        # TODO(EA2D): Can share with NDArrayBackedExtensionBlock
        new_values = algos.diff(self.values, n, axis=0)
        return [self.make_block(values=new_values)]

    @final
    def diff(self, n: int) -> list[Block]:
        """return block for the diff of the values"""
        # only reached with ndim == 2
        # TODO(EA2D): transpose will be unnecessary with 2D EAs
        new_values = algos.diff(self.values.T, n, axis=0).T
        return [self.make_block(values=new_values)]

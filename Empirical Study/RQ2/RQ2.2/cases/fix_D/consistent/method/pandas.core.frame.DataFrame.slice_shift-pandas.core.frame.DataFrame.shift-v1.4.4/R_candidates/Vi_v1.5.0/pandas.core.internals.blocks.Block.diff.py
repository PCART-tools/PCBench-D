    def diff(self, n: int, axis: int = 1) -> list[Block]:
        """return block for the diff of the values"""
        new_values = algos.diff(self.values, n, axis=axis)
        return [self.make_block(values=new_values)]

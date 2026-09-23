    @final
    def reduce(self, func) -> list[Block]:
        # We will apply the function and reshape the result into a single-row
        #  Block with the same mgr_locs; squeezing will be done at a higher level
        assert self.ndim == 2

        result = func(self.values)

        if self.values.ndim == 1:
            # TODO(EA2D): special case not needed with 2D EAs
            res_values = np.array([[result]])
        else:
            res_values = result.reshape(-1, 1)

        nb = self.make_block(res_values)
        return [nb]

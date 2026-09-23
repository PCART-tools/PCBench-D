    def interpolate(self: T, **kwargs) -> T:
        return self.apply_with_block("interpolate", swap_axis=False, **kwargs)

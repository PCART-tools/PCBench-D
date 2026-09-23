    def nonsingular(self, vmin, vmax):
        # docstring inherited
        return ((0, 1) if (vmin, vmax) == (-np.inf, np.inf)  # Init. limits.
                else self.base.nonsingular(vmin, vmax))

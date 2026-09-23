    def interpolated(self, steps):
        """
        Returns a new path resampled to length N x steps.  Does not
        currently handle interpolating curves.
        """
        if steps == 1:
            return self

        vertices = simple_linear_interpolation(self.vertices, steps)
        codes = self.codes
        if codes is not None:
            new_codes = Path.LINETO * np.ones(((len(codes) - 1) * steps + 1, ))
            new_codes[0::steps] = codes
        else:
            new_codes = None
        return Path(vertices, new_codes)

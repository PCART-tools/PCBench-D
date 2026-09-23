    @cacheit
    def _inverse_cdf_expression(self):
        """ Inverse of the CDF

        Used by sample
        """
        x = Dummy('x', positive=True, integer=True)
        z = Dummy('z', positive=True)
        cdf_temp = self.cdf(x)
        # Invert CDF
        try:
            inverse_cdf = solveset(cdf_temp - z, x, domain=S.Reals)
        except NotImplementedError:
            inverse_cdf = None
        if not inverse_cdf or len(inverse_cdf.free_symbols) != 1:
            raise NotImplementedError("Could not invert CDF")
        return Lambda(z, inverse_cdf)

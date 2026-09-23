    @_api.rename_parameter("3.8", "a", "values")
    def transform_non_affine(self, values):
        """logit transform (base 10), masked or clipped"""
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.log10(values / (1 - values))
        if self._clip:  # See LogTransform for choice of clip value.
            out[values <= 0] = -1000
            out[1 <= values] = 1000
        return out

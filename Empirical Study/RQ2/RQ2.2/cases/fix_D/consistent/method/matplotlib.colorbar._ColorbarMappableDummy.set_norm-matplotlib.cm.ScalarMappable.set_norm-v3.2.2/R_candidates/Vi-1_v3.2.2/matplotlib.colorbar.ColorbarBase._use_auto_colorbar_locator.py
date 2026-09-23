    def _use_auto_colorbar_locator(self):
        """
        Return if we should use an adjustable tick locator or a fixed
        one.  (check is used twice so factored out here...)
        """
        contouring = self.boundaries is not None and self.spacing == 'uniform'
        return (type(self.norm) in [colors.Normalize, colors.LogNorm] and
                not contouring)

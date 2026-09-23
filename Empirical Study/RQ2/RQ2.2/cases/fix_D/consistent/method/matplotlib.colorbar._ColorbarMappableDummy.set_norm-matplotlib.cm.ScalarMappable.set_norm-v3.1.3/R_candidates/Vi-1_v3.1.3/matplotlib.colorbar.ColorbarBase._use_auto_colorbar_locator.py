    def _use_auto_colorbar_locator(self):
        """
        Return if we should use an adjustable tick locator or a fixed
        one.  (check is used twice so factored out here...)
        """
        return (self.boundaries is None
                and self.values is None
                and ((type(self.norm) == colors.Normalize)
                    or (type(self.norm) == colors.LogNorm)))

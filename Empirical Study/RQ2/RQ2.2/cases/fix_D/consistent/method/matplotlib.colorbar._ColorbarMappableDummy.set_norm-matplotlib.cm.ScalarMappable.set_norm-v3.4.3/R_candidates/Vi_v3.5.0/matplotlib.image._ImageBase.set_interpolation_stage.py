    def set_interpolation_stage(self, s):
        """
        Set when interpolation happens during the transform to RGBA.

        Parameters
        ----------
        s : {'data', 'rgba'} or None
            Whether to apply up/downsampling interpolation in data or rgba
            space.
        """
        if s is None:
            s = "data"  # placeholder for maybe having rcParam
        _api.check_in_list(['data', 'rgba'])
        self._interpolation_stage = s
        self.stale = True

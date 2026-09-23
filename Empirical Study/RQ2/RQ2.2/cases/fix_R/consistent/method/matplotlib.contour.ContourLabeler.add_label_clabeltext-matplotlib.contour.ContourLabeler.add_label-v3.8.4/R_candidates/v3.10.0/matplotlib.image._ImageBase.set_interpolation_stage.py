    def set_interpolation_stage(self, s):
        """
        Set when interpolation happens during the transform to RGBA.

        Parameters
        ----------
        s : {'data', 'rgba', 'auto'} or None
            Whether to apply up/downsampling interpolation in data or RGBA
            space.  If None, use :rc:`image.interpolation_stage`.
            If 'auto' we will check upsampling rate and if less
            than 3 then use 'rgba', otherwise use 'data'.
        """
        s = mpl._val_or_rc(s, 'image.interpolation_stage')
        _api.check_in_list(['data', 'rgba', 'auto'], s=s)
        self._interpolation_stage = s
        self.stale = True

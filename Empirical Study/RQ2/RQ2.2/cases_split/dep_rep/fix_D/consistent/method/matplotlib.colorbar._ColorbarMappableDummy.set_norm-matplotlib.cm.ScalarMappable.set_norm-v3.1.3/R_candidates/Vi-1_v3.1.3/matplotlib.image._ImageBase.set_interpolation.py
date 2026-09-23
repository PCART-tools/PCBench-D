    def set_interpolation(self, s):
        """
        Set the interpolation method the image uses when resizing.

        if None, use a value from rc setting. If 'none', the image is
        shown as is without interpolating. 'none' is only supported in
        agg, ps and pdf backends and will fall back to 'nearest' mode
        for other backends.

        Parameters
        ----------
        s : {'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', \
'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', \
'bessel', 'mitchell', 'sinc', 'lanczos', 'none'}

        """
        if s is None:
            s = rcParams['image.interpolation']
        s = s.lower()
        if s not in _interpd_:
            raise ValueError('Illegal interpolation string')
        self._interpolation = s
        self.stale = True

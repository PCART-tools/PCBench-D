    def set_interpolation(self, s):
        """
        Parameters
        ----------
        s : str, None
            Either 'nearest', 'bilinear', or ``None``.
        """
        if s is not None and s not in ('nearest', 'bilinear'):
            raise NotImplementedError('Only nearest neighbor and '
                                      'bilinear interpolations are supported')
        AxesImage.set_interpolation(self, s)

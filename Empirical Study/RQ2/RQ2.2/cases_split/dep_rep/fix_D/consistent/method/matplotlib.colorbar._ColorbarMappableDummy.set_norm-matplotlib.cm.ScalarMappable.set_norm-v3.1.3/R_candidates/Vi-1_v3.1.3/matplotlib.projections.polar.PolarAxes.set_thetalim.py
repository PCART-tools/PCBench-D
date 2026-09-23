    def set_thetalim(self, *args, **kwargs):
        """
        Set the minimum and maximum theta values.

        Parameters
        ----------
        thetamin : float
            Minimum value in degrees.
        thetamax : float
            Maximum value in degrees.
        """
        if 'thetamin' in kwargs:
            kwargs['xmin'] = np.deg2rad(kwargs.pop('thetamin'))
        if 'thetamax' in kwargs:
            kwargs['xmax'] = np.deg2rad(kwargs.pop('thetamax'))
        return tuple(np.rad2deg(self.set_xlim(*args, **kwargs)))

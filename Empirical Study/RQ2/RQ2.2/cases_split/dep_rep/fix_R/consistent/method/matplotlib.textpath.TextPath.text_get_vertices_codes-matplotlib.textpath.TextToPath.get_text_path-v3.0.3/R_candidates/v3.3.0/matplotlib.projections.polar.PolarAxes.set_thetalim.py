    def set_thetalim(self, *args, **kwargs):
        r"""
        Set the minimum and maximum theta values.

        Can take the following signatures:

        - ``set_thetalim(minval, maxval)``: Set the limits in radians.
        - ``set_thetalim(thetamin=minval, thetamax=maxval)``: Set the limits
          in degrees.

        where minval and maxval are the minimum and maximum limits. Values are
        wrapped in to the range :math:`[0, 2\pi]` (in radians), so for example
        it is possible to do ``set_thetalim(-np.pi / 2, np.pi / 2)`` to have
        an axes symmetric around 0. A ValueError is raised if the absolute
        angle difference is larger than :math:`2\pi`.
        """
        thetamin = None
        thetamax = None
        left = None
        right = None

        if len(args) == 2:
            if args[0] is not None and args[1] is not None:
                left, right = args
                if abs(right - left) > 2 * np.pi:
                    raise ValueError('The angle range must be <= 2 pi')

        if 'thetamin' in kwargs:
            thetamin = np.deg2rad(kwargs.pop('thetamin'))
        if 'thetamax' in kwargs:
            thetamax = np.deg2rad(kwargs.pop('thetamax'))

        if thetamin is not None and thetamax is not None:
            if abs(thetamax - thetamin) > 2 * np.pi:
                raise ValueError('The angle range must be <= 360 degrees')
        return tuple(np.rad2deg(self.set_xlim(left=left, right=right,
                                              xmin=thetamin, xmax=thetamax)))

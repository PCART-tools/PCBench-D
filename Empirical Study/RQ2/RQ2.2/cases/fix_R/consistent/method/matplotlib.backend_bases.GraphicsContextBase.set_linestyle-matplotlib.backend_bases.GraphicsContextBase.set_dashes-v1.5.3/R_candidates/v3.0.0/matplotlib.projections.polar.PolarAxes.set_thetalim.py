    def set_thetalim(self, *args, **kwargs):
        if 'thetamin' in kwargs:
            kwargs['xmin'] = np.deg2rad(kwargs.pop('thetamin'))
        if 'thetamax' in kwargs:
            kwargs['xmax'] = np.deg2rad(kwargs.pop('thetamax'))
        return tuple(np.rad2deg(self.set_xlim(*args, **kwargs)))

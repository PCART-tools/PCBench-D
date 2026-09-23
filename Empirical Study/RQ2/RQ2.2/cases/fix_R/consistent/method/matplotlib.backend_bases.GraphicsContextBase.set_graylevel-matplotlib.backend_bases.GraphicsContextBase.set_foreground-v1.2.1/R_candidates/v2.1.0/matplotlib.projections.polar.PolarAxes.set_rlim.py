    def set_rlim(self, *args, **kwargs):
        if 'rmin' in kwargs:
            kwargs['ymin'] = kwargs.pop('rmin')
        if 'rmax' in kwargs:
            kwargs['ymax'] = kwargs.pop('rmax')
        return self.set_ylim(*args, **kwargs)

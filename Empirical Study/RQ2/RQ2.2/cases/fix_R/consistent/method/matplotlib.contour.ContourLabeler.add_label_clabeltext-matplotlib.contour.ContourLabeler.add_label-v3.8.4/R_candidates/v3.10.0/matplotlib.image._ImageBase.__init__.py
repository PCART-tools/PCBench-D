    def __init__(self, ax,
                 cmap=None,
                 norm=None,
                 colorizer=None,
                 interpolation=None,
                 origin=None,
                 filternorm=True,
                 filterrad=4.0,
                 resample=False,
                 *,
                 interpolation_stage=None,
                 **kwargs
                 ):
        super().__init__(self._get_colorizer(cmap, norm, colorizer))
        if origin is None:
            origin = mpl.rcParams['image.origin']
        _api.check_in_list(["upper", "lower"], origin=origin)
        self.origin = origin
        self.set_filternorm(filternorm)
        self.set_filterrad(filterrad)
        self.set_interpolation(interpolation)
        self.set_interpolation_stage(interpolation_stage)
        self.set_resample(resample)
        self.axes = ax

        self._imcache = None

        self._internal_update(kwargs)

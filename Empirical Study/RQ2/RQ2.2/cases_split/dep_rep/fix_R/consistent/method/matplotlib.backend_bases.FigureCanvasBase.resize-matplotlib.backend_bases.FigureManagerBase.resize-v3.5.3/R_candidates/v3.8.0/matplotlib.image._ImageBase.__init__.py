    def __init__(self, ax,
                 cmap=None,
                 norm=None,
                 interpolation=None,
                 origin=None,
                 filternorm=True,
                 filterrad=4.0,
                 resample=False,
                 *,
                 interpolation_stage=None,
                 **kwargs
                 ):
        martist.Artist.__init__(self)
        cm.ScalarMappable.__init__(self, norm, cmap)
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

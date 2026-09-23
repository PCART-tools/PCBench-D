    def __init__(self, axis=None, use_rmin=True,
                 _apply_theta_transforms=True):
        mtransforms.Transform.__init__(self)
        self._axis = axis
        self._use_rmin = use_rmin
        self._apply_theta_transforms = _apply_theta_transforms

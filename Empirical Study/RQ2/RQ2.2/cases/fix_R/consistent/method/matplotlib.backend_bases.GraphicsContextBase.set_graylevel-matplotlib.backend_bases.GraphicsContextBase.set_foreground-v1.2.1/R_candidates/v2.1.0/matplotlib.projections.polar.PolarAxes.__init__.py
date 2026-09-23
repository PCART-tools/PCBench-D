    def __init__(self, *args, **kwargs):
        """
        Create a new Polar Axes for a polar plot.
        """
        self._default_theta_offset = kwargs.pop('theta_offset', 0)
        self._default_theta_direction = kwargs.pop('theta_direction', 1)
        self._default_rlabel_position = np.deg2rad(
            kwargs.pop('rlabel_position', 22.5))

        Axes.__init__(self, *args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.cla()

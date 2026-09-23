    def __init__(self, axes, pickradius=15):
        """
        Init the axis with the parent Axes instance
        """
        artist.Artist.__init__(self)
        self.set_figure(axes.figure)

        self.isDefault_label = True

        self.axes = axes
        self.major = Ticker()
        self.minor = Ticker()
        self.callbacks = cbook.CallbackRegistry()

        self._autolabelpos = True
        self._smart_bounds = False

        self.label = self._get_label()
        self.labelpad = rcParams['axes.labelpad']
        self.offsetText = self._get_offset_text()

        self.pickradius = pickradius

        # Initialize here for testing; later add API
        self._major_tick_kw = dict()
        self._minor_tick_kw = dict()

        self.cla()
        self._set_scale('linear')

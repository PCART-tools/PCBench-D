    @classmethod
    def _setup_axes(cls, axes, info_axis=None, stat_axis=None, aliases=None,
                    slicers=None, axes_are_reversed=False, build_axes=True,
                    ns=None):
        """Provide axes setup for the major PandasObjects.

        Parameters
        ----------
        axes : the names of the axes in order (lowest to highest)
        info_axis_num : the axis of the selector dimension (int)
        stat_axis_num : the number of axis for the default stats (int)
        aliases : other names for a single axis (dict)
        slicers : how axes slice to others (dict)
        axes_are_reversed : boolean whether to treat passed axes as
            reversed (DataFrame)
        build_axes : setup the axis properties (default True)
        """

        cls._AXIS_ORDERS = axes
        cls._AXIS_NUMBERS = dict((a, i) for i, a in enumerate(axes))
        cls._AXIS_LEN = len(axes)
        cls._AXIS_ALIASES = aliases or dict()
        cls._AXIS_IALIASES = dict((v, k) for k, v in cls._AXIS_ALIASES.items())
        cls._AXIS_NAMES = dict(enumerate(axes))
        cls._AXIS_SLICEMAP = slicers or None
        cls._AXIS_REVERSED = axes_are_reversed

        # typ
        setattr(cls, '_typ', cls.__name__.lower())

        # indexing support
        cls._ix = None

        if info_axis is not None:
            cls._info_axis_number = info_axis
            cls._info_axis_name = axes[info_axis]

        if stat_axis is not None:
            cls._stat_axis_number = stat_axis
            cls._stat_axis_name = axes[stat_axis]

        # setup the actual axis
        if build_axes:

            def set_axis(a, i):
                setattr(cls, a, properties.AxisProperty(i))
                cls._internal_names_set.add(a)

            if axes_are_reversed:
                m = cls._AXIS_LEN - 1
                for i, a in cls._AXIS_NAMES.items():
                    set_axis(a, m - i)
            else:
                for i, a in cls._AXIS_NAMES.items():
                    set_axis(a, i)

        # addtl parms
        if isinstance(ns, dict):
            for k, v in ns.items():
                setattr(cls, k, v)

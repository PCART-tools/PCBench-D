    @classmethod
    def _setup_axes(cls, axes: List[str], docs: Dict[str, str]) -> None:
        """
        Provide axes setup for the major PandasObjects.

        Parameters
        ----------
        axes : the names of the axes in order (lowest to highest)
        docs : docstrings for the axis properties
        """
        info_axis = len(axes) - 1
        axes_are_reversed = len(axes) > 1

        cls._AXIS_ORDERS = axes
        cls._AXIS_NUMBERS = {a: i for i, a in enumerate(axes)}
        cls._AXIS_LEN = len(axes)
        cls._AXIS_NAMES = dict(enumerate(axes))
        cls._AXIS_REVERSED = axes_are_reversed

        cls._info_axis_number = info_axis
        cls._info_axis_name = axes[info_axis]

        # setup the actual axis
        def set_axis(a, i):
            setattr(cls, a, properties.AxisProperty(i, docs.get(a, a)))
            cls._internal_names_set.add(a)

        if axes_are_reversed:
            for i, a in cls._AXIS_NAMES.items():
                set_axis(a, 1 - i)
        else:
            for i, a in cls._AXIS_NAMES.items():
                set_axis(a, i)

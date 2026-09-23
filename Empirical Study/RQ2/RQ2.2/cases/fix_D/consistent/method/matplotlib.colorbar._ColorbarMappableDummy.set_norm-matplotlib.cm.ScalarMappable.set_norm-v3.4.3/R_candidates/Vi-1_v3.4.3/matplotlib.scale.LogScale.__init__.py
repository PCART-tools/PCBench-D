    def __init__(self, axis, **kwargs):
        """
        Parameters
        ----------
        axis : `~matplotlib.axis.Axis`
            The axis for the scale.
        base : float, default: 10
            The base of the logarithm.
        nonpositive : {'clip', 'mask'}, default: 'clip'
            Determines the behavior for non-positive values. They can either
            be masked as invalid, or clipped to a very small positive number.
        subs : sequence of int, default: None
            Where to place the subticks between each major tick.  For example,
            in a log10 scale, ``[2, 3, 4, 5, 6, 7, 8, 9]`` will place 8
            logarithmically spaced minor ticks between each major tick.
        """
        # After the deprecation, the whole (outer) __init__ can be replaced by
        # def __init__(self, axis, *, base=10, subs=None, nonpositive="clip")
        # The following is to emit the right warnings depending on the axis
        # used, as the *old* kwarg names depended on the axis.
        axis_name = getattr(axis, "axis_name", "x")
        @_api.rename_parameter("3.3", f"base{axis_name}", "base")
        @_api.rename_parameter("3.3", f"subs{axis_name}", "subs")
        @_api.rename_parameter("3.3", f"nonpos{axis_name}", "nonpositive")
        def __init__(*, base=10, subs=None, nonpositive="clip"):
            return base, subs, nonpositive

        base, subs, nonpositive = __init__(**kwargs)
        self._transform = LogTransform(base, nonpositive)
        self.subs = subs

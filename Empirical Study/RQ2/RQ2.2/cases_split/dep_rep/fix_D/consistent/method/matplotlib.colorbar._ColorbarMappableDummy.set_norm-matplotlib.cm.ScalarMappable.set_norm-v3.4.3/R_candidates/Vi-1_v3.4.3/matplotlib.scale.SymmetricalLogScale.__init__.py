    def __init__(self, axis, **kwargs):
        axis_name = getattr(axis, "axis_name", "x")
        # See explanation in LogScale.__init__.
        @_api.rename_parameter("3.3", f"base{axis_name}", "base")
        @_api.rename_parameter("3.3", f"linthresh{axis_name}", "linthresh")
        @_api.rename_parameter("3.3", f"subs{axis_name}", "subs")
        @_api.rename_parameter("3.3", f"linscale{axis_name}", "linscale")
        def __init__(*, base=10, linthresh=2, subs=None, linscale=1):
            return base, linthresh, subs, linscale

        base, linthresh, subs, linscale = __init__(**kwargs)
        self._transform = SymmetricalLogTransform(base, linthresh, linscale)
        self.subs = subs

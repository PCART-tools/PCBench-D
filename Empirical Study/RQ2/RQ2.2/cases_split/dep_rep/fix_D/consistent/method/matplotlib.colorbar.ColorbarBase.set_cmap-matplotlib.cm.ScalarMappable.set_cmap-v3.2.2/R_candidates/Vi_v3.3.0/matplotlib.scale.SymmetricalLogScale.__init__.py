    def __init__(self, axis, **kwargs):
        axis_name = getattr(axis, "axis_name", "x")
        # See explanation in LogScale.__init__.
        @cbook._rename_parameter("3.3", f"base{axis_name}", "base")
        @cbook._rename_parameter("3.3", f"linthresh{axis_name}", "linthresh")
        @cbook._rename_parameter("3.3", f"subs{axis_name}", "subs")
        @cbook._rename_parameter("3.3", f"linscale{axis_name}", "linscale")
        def __init__(*, base=10, linthresh=2, subs=None, linscale=1, **kwargs):
            if kwargs:
                warn_deprecated(
                    '3.2', removal='3.4',
                    message=(
                        f"SymmetricalLogScale got an unexpected keyword "
                        f"argument {next(iter(kwargs))!r}. This will become "
                        "an error %(removal)s.")
                )
            return base, linthresh, subs, linscale

        base, linthresh, subs, linscale = __init__(**kwargs)
        self._transform = SymmetricalLogTransform(base, linthresh, linscale)
        self.subs = subs

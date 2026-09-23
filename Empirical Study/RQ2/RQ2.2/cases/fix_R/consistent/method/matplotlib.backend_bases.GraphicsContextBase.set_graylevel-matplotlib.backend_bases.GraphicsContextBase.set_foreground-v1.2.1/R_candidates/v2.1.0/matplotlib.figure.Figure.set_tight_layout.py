    def set_tight_layout(self, tight):
        """
        Set whether :meth:`tight_layout` is used upon drawing.
        If None, the rcParams['figure.autolayout'] value will be set.

        When providing a dict containing the keys `pad`, `w_pad`, `h_pad`
        and `rect`, the default :meth:`tight_layout` paddings will be
        overridden.

        ACCEPTS: [True | False | dict | None ]
        """
        if tight is None:
            tight = rcParams['figure.autolayout']
        self._tight = bool(tight)
        self._tight_parameters = tight if isinstance(tight, dict) else {}
        self.stale = True

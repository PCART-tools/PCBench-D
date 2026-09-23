    def set_tight_layout(self, tight):
        """
        Set whether and how `.tight_layout` is called when drawing.

        Parameters
        ----------
        tight : bool or dict with keys "pad", "w_pad", "h_pad", "rect" or None
            If a bool, sets whether to call `.tight_layout` upon drawing.
            If ``None``, use the ``figure.autolayout`` rcparam instead.
            If a dict, pass it as kwargs to `.tight_layout`, overriding the
            default paddings.
        """
        if tight is None:
            tight = rcParams['figure.autolayout']
        self._tight = bool(tight)
        self._tight_parameters = tight if isinstance(tight, dict) else {}
        self.stale = True

    @_api.deprecated("3.6", alternative="set_layout_engine",
                     pending=True)
    def set_tight_layout(self, tight):
        """
        Set whether and how `.tight_layout` is called when drawing.

        Parameters
        ----------
        tight : bool or dict with keys "pad", "w_pad", "h_pad", "rect" or None
            If a bool, sets whether to call `.tight_layout` upon drawing.
            If ``None``, use :rc:`figure.autolayout` instead.
            If a dict, pass it as kwargs to `.tight_layout`, overriding the
            default paddings.
        """
        if tight is None:
            tight = mpl.rcParams['figure.autolayout']
        _tight = 'tight' if bool(tight) else 'none'
        _tight_parameters = tight if isinstance(tight, dict) else {}
        self.set_layout_engine(_tight, **_tight_parameters)
        self.stale = True

    def __init__(self, xpad=0., ypad=0., update_func=None):
        """
        Parameters
        ----------
        xpad : float, optional
            Padding in x-direction.
        ypad : float, optional
            Padding in y-direction.
        update_func : callable, optional
            Function for updating the legend handler properties from another
            legend handler, used by `~HandlerBase.update_prop`.
        """
        self._xpad, self._ypad = xpad, ypad
        self._update_prop_func = update_func

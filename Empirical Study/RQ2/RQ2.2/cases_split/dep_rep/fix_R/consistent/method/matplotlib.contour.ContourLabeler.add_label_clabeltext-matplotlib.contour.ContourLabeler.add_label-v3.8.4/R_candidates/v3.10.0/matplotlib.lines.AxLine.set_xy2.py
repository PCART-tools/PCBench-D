    def set_xy2(self, *args, **kwargs):
        """
        Set the *xy2* value of the line.

        .. note::

            You can only set *xy2* if the line was created using the *xy2*
            parameter. If the line was created using *slope*, please use
            `~.AxLine.set_slope`.

        Parameters
        ----------
        xy2 : tuple[float, float]
            Points for the line to pass through.
        """
        if self._slope is None:
            params = _api.select_matching_signature([
                lambda self, x, y: locals(), lambda self, xy2: locals(),
            ], self, *args, **kwargs)
            if "x" in params:
                _api.warn_deprecated("3.10", message=(
                    "Passing x and y separately to AxLine.set_xy2 is deprecated since "
                    "%(since)s; pass them as a single tuple instead."))
                xy2 = params["x"], params["y"]
            else:
                xy2 = params["xy2"]
            self._xy2 = xy2
        else:
            raise ValueError("Cannot set an 'xy2' value while 'slope' is set;"
                             " they differ but their functionalities overlap")

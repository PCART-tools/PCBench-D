    def set_dashes(self, dash_offset, dash_list):
        """
        Set the dash style for the gc.

        Parameters
        ----------
        dash_offset : float
            is the offset (usually 0).

        dash_list : array_like
            specifies the on-off sequence as points.
            ``(None, None)`` specifies a solid line

        """
        if dash_list is not None:
            dl = np.asarray(dash_list)
            if np.any(dl < 0.0):
                raise ValueError(
                    "All values in the dash list must be positive")
        self._dashes = dash_offset, dash_list

    def _putmask(self, mask: npt.NDArray[np.bool_], value) -> None:
        """
        Analogue to np.putmask(self, mask, value)

        Parameters
        ----------
        mask : np.ndarray[bool]
        value : scalar or listlike
            If listlike, must be arraylike with same length as self.

        Returns
        -------
        None

        Notes
        -----
        Unlike np.putmask, we do not repeat listlike values with mismatched length.
        'value' should either be a scalar or an arraylike with the same length
        as self.
        """
        if is_list_like(value):
            val = value[mask]
        else:
            val = value

        self[mask] = val

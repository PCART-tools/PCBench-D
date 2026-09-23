    def _where(self, mask: npt.NDArray[np.bool_], value) -> Self:
        """
        Analogue to np.where(mask, self, value)

        Parameters
        ----------
        mask : np.ndarray[bool]
        value : scalar or listlike

        Returns
        -------
        same type as self
        """
        result = self.copy()

        if is_list_like(value):
            val = value[~mask]
        else:
            val = value

        result[~mask] = val
        return result

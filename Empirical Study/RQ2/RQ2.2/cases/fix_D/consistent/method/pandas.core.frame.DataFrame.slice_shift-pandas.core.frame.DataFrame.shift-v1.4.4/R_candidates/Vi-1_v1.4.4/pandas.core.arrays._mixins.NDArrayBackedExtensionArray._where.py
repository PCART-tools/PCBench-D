    def _where(
        self: NDArrayBackedExtensionArrayT, mask: np.ndarray, value
    ) -> NDArrayBackedExtensionArrayT:
        """
        Analogue to np.where(mask, self, value)

        Parameters
        ----------
        mask : np.ndarray[bool]
        value : scalar or listlike

        Raises
        ------
        TypeError
            If value cannot be cast to self.dtype.
        """
        value = self._validate_setitem_value(value)

        res_values = np.where(mask, self._ndarray, value)
        return self._from_backing_data(res_values)

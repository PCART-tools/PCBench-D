    @property
    def values(self) -> np.ndarray:
        # NB: For Datetime64TZ this is lossy
        data = self._data._ndarray
        if using_copy_on_write():
            data = data.view()
            data.flags.writeable = False
        return data

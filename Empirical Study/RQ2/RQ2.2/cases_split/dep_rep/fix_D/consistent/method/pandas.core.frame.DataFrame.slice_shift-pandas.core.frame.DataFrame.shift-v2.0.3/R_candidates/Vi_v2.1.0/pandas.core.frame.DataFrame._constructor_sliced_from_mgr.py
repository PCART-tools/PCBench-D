    def _constructor_sliced_from_mgr(self, mgr, axes):
        ser = self._sliced_from_mgr(mgr, axes=axes)
        ser._name = None  # caller is responsible for setting real name
        if type(self) is DataFrame:
            # fastpath avoiding constructor call
            return ser
        assert axes is mgr.axes
        return self._constructor_sliced(ser, copy=False)

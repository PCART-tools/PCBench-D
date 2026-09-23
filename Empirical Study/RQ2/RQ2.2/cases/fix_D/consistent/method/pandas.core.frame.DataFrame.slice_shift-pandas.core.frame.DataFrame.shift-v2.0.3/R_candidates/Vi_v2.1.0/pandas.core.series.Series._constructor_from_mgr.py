    def _constructor_from_mgr(self, mgr, axes):
        ser = self._from_mgr(mgr, axes=axes)
        ser._name = None  # caller is responsible for setting real name
        if type(self) is Series:
            # fastpath avoiding constructor call
            return ser
        else:
            assert axes is mgr.axes
            return self._constructor(ser, copy=False)

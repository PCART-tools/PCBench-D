    def _constructor_expanddim_from_mgr(self, mgr, axes):
        df = self._expanddim_from_mgr(mgr, axes)
        if type(self) is Series:
            # fastpath avoiding constructor
            return df
        assert axes is mgr.axes
        return self._constructor_expanddim(df, copy=False)

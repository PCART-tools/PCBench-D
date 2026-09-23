    def _constructor_from_mgr(self, mgr, axes):
        df = self._from_mgr(mgr, axes=axes)

        if type(self) is DataFrame:
            # fastpath avoiding constructor call
            return df
        else:
            assert axes is mgr.axes
            return self._constructor(df, copy=False)

    def _astype(self, dtype, copy=False, raise_on_error=True, values=None,
                klass=None):
        """
        Coerce to the new type (if copy=True, return a new copy)
        raise on an except if raise == True
        """

        if dtype == com.CategoricalDtype():
            values = self.values
        else:
            values = np.array(self.values).astype(dtype)

        if copy:
            values = values.copy()

        return make_block(values,
                          ndim=self.ndim,
                          placement=self.mgr_locs)

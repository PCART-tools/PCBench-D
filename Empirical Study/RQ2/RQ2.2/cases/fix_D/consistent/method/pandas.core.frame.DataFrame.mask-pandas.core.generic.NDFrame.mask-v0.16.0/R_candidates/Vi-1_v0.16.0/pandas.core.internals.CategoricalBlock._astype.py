    def _astype(self, dtype, copy=False, raise_on_error=True, values=None,
                klass=None):
        """
        Coerce to the new type (if copy=True, return a new copy)
        raise on an except if raise == True
        """

        if self.is_categorical_astype(dtype):
            values = self.values
        else:
            values = np.asarray(self.values).astype(dtype, copy=False)

        if copy:
            values = values.copy()

        return make_block(values,
                          ndim=self.ndim,
                          placement=self.mgr_locs)

    def _astype(self, dtype, copy=False, errors='raise', values=None,
                klass=None, mgr=None):
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

        return self.make_block(values)

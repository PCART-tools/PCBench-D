    def find(self, dtype):
        """
        Parameters
        ----------
        dtype : PandasExtensionDtype or string

        Returns
        -------
        return the first matching dtype, otherwise return None
        """
        if not isinstance(dtype, compat.string_types):
            dtype_type = dtype
            if not isinstance(dtype, type):
                dtype_type = type(dtype)
            if issubclass(dtype_type, ExtensionDtype):
                return dtype

            return None

        for dtype_type in self.dtypes:
            try:
                return dtype_type.construct_from_string(dtype)
            except TypeError:
                pass

        return None

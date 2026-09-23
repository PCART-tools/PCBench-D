    def find(
        self, dtype: type_t[ExtensionDtype] | ExtensionDtype | npt.DTypeLike
    ) -> type_t[ExtensionDtype] | ExtensionDtype | None:
        """
        Parameters
        ----------
        dtype : ExtensionDtype class or instance or str or numpy dtype or python type

        Returns
        -------
        return the first matching dtype, otherwise return None
        """
        if not isinstance(dtype, str):
            dtype_type: type_t
            if not isinstance(dtype, type):
                dtype_type = type(dtype)
            else:
                dtype_type = dtype
            if issubclass(dtype_type, ExtensionDtype):
                # cast needed here as mypy doesn't know we have figured
                # out it is an ExtensionDtype or type_t[ExtensionDtype]
                return cast("ExtensionDtype | type_t[ExtensionDtype]", dtype)

            return None

        for dtype_type in self.dtypes:
            try:
                return dtype_type.construct_from_string(dtype)
            except TypeError:
                pass

        return None

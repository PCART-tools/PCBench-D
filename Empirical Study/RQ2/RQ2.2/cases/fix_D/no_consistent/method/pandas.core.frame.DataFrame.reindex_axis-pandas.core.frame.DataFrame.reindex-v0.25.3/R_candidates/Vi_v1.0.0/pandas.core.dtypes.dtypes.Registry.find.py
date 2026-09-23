    def find(
        self, dtype: Union[Type[ExtensionDtype], str]
    ) -> Optional[Type[ExtensionDtype]]:
        """
        Parameters
        ----------
        dtype : Type[ExtensionDtype] or str

        Returns
        -------
        return the first matching dtype, otherwise return None
        """
        if not isinstance(dtype, str):
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

    def register(self, dtype: type_t[ExtensionDtype]) -> None:
        """
        Parameters
        ----------
        dtype : ExtensionDtype class
        """
        if not issubclass(dtype, ExtensionDtype):
            raise ValueError("can only register pandas extension dtypes")

        self.dtypes.append(dtype)

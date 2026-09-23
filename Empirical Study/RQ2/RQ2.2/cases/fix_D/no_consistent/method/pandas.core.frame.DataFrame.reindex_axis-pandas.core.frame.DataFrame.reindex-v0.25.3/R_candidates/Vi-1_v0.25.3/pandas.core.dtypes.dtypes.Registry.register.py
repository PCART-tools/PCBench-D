    def register(self, dtype: Type[ExtensionDtype]) -> None:
        """
        Parameters
        ----------
        dtype : ExtensionDtype
        """
        if not issubclass(dtype, ExtensionDtype):
            raise ValueError("can only register pandas extension dtypes")

        self.dtypes.append(dtype)

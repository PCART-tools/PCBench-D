    def register(self, dtype):
        """
        Parameters
        ----------
        dtype : ExtensionDtype
        """
        if not issubclass(dtype, (PandasExtensionDtype, ExtensionDtype)):
            raise ValueError("can only register pandas extension dtypes")

        self.dtypes.append(dtype)

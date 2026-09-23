    @property
    def type(self):
        """
        Returns pyarrow.DataType.
        """
        return type(self.pyarrow_dtype)

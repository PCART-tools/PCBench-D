    def _disabled(self, *args, **kwargs) -> NoReturn:
        """
        This method will not function because object is immutable.
        """
        raise TypeError(f"'{type(self).__name__}' does not support mutable operations.")

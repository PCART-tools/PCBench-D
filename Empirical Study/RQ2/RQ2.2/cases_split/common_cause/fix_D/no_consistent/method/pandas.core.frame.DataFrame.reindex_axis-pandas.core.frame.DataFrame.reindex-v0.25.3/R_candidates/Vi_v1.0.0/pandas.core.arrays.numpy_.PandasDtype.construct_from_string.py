    @classmethod
    def construct_from_string(cls, string):
        try:
            return cls(np.dtype(string))
        except TypeError as err:
            raise TypeError(
                f"Cannot construct a 'PandasDtype' from '{string}'"
            ) from err

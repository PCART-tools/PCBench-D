    @classmethod
    def construct_from_string(cls, string: str) -> "PandasDtype":
        try:
            dtype = np.dtype(string)
        except TypeError as err:
            if not isinstance(string, str):
                msg = f"'construct_from_string' expects a string, got {type(string)}"
            else:
                msg = f"Cannot construct a 'PandasDtype' from '{string}'"
            raise TypeError(msg) from err
        return cls(dtype)

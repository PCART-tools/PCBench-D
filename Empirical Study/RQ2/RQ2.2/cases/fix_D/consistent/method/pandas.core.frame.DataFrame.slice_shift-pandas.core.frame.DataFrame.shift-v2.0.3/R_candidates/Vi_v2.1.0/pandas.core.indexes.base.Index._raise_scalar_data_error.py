    @final
    @classmethod
    def _raise_scalar_data_error(cls, data):
        # We return the TypeError so that we can raise it from the constructor
        #  in order to keep mypy happy
        raise TypeError(
            f"{cls.__name__}(...) must be called with a collection of some "
            f"kind, {repr(data) if not isinstance(data, np.generic) else str(data)} "
            "was passed"
        )

    @classmethod
    def _scalar_data_error(cls, data):
        # We return the TypeError so that we can raise it from the constructor
        #  in order to keep mypy happy
        return TypeError(
            f"{cls.__name__}(...) must be called with a collection of some "
            f"kind, {repr(data)} was passed"
        )

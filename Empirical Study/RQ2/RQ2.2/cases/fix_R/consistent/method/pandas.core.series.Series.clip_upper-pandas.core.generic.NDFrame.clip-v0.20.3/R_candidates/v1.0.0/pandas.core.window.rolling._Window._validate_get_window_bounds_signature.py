    @staticmethod
    def _validate_get_window_bounds_signature(window: BaseIndexer) -> None:
        """
        Validate that the passed BaseIndexer subclass has
        a get_window_bounds with the correct signature.
        """
        get_window_bounds_signature = inspect.signature(
            window.get_window_bounds
        ).parameters.keys()
        expected_signature = inspect.signature(
            BaseIndexer().get_window_bounds
        ).parameters.keys()
        if get_window_bounds_signature != expected_signature:
            raise ValueError(
                f"{type(window).__name__} does not implement the correct signature for "
                f"get_window_bounds"
            )

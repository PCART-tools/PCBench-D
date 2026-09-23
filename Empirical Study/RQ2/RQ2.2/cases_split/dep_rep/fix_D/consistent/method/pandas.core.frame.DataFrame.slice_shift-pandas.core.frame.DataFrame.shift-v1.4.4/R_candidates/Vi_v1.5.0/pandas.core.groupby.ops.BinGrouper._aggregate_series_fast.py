    def _aggregate_series_fast(self, obj: Series, func: Callable) -> NoReturn:
        # -> np.ndarray[object]
        raise NotImplementedError(
            "This should not be reached; use _aggregate_series_pure_python"
        )

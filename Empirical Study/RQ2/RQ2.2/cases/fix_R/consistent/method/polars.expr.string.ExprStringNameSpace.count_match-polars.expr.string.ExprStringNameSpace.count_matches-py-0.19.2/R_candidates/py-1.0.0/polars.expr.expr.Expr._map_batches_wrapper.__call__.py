        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            result = self.function(*args, **kwargs)
            if _check_for_numpy(result) and isinstance(result, np.ndarray):
                result = pl.Series(result, dtype=self.return_dtype)
            return result

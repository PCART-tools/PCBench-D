    def __array_finalize__(self, obj: Any) -> None:
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.owned_series = getattr(obj, "owned_series", None)

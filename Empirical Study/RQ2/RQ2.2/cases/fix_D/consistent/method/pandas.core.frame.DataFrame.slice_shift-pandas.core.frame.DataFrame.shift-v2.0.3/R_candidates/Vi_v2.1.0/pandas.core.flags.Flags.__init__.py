    def __init__(self, obj: NDFrame, *, allows_duplicate_labels: bool) -> None:
        self._allows_duplicate_labels = allows_duplicate_labels
        self._obj = weakref.ref(obj)

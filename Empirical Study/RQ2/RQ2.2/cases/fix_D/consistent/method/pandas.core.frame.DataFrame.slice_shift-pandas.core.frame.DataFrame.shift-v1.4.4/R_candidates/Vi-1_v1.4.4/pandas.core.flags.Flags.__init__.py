    def __init__(self, obj, *, allows_duplicate_labels):
        self._allows_duplicate_labels = allows_duplicate_labels
        self._obj = weakref.ref(obj)

    def _set_is_copy(self, ref=None, copy=True):
        if not copy:
            self._is_copy = None
        else:
            if ref is not None:
                self._is_copy = weakref.ref(ref)
            else:
                self._is_copy = None

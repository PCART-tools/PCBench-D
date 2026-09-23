    def _set_is_copy(self, ref=None, copy=True):
        if not copy:
            self.is_copy = None
        else:
            if ref is not None:
                self.is_copy = weakref.ref(ref)
            else:
                self.is_copy = None

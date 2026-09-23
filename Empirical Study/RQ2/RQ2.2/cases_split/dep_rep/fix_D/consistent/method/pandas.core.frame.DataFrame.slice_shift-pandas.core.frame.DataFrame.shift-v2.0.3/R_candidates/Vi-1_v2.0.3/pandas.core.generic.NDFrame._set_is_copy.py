    @final
    def _set_is_copy(self, ref: NDFrame, copy: bool_t = True) -> None:
        if not copy:
            self._is_copy = None
        else:
            assert ref is not None
            self._is_copy = weakref.ref(ref)

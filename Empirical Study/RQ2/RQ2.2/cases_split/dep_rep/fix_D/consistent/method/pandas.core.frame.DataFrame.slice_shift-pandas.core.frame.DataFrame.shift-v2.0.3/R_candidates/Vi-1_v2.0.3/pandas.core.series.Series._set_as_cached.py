    def _set_as_cached(self, item, cacher) -> None:
        """
        Set the _cacher attribute on the calling object with a weakref to
        cacher.
        """
        if using_copy_on_write():
            return
        self._cacher = (item, weakref.ref(cacher))

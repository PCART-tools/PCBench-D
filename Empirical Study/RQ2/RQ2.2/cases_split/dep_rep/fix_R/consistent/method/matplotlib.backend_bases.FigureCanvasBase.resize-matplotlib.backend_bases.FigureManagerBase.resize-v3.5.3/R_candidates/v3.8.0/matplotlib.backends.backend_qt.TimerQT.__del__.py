    def __del__(self):
        # The check for deletedness is needed to avoid an error at animation
        # shutdown with PySide2.
        if not _isdeleted(self._timer):
            self._timer_stop()

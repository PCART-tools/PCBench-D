    def __del__(self):
        """Need to stop timer and possibly disconnect timer."""
        self._timer_stop()

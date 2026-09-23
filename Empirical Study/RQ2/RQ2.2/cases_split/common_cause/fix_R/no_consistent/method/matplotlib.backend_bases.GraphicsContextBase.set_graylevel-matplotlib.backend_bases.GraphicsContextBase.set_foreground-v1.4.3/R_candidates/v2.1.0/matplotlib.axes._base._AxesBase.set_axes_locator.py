    def set_axes_locator(self, locator):
        """
        set axes_locator

        ACCEPT: a callable object which takes an axes instance and renderer and
                 returns a bbox.
        """
        self._axes_locator = locator
        self.stale = True

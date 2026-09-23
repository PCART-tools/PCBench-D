    @minorlocator.setter
    def minorlocator(self, loc):
        self._long_axis().set_minor_locator(loc)
        self._minorlocator = loc

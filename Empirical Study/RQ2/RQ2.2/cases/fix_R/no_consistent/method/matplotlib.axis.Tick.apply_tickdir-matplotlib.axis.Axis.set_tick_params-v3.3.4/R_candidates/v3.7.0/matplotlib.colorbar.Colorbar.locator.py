    @locator.setter
    def locator(self, loc):
        self._long_axis().set_major_locator(loc)
        self._locator = loc

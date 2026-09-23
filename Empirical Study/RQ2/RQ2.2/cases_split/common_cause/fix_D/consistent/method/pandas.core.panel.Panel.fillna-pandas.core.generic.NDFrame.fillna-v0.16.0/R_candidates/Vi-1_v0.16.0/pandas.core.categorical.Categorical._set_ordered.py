    def _set_ordered(self, value):
        """ Sets the ordered attribute to the boolean value """
        warn("Setting 'ordered' directly is deprecated, use 'set_ordered'", FutureWarning)
        self.set_ordered(value, inplace=True)

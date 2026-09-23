    def set_useOffset(self, val):
        if val in [True, False]:
            self.offset = 0
            self._useOffset = val
        else:
            self._useOffset = False
            self.offset = val

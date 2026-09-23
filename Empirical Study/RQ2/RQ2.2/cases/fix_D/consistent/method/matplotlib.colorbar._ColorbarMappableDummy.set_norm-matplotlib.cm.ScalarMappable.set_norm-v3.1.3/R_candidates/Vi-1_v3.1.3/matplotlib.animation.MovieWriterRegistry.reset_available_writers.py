    def reset_available_writers(self):
        """Reset the available state of all registered writers"""
        self.avail = {name: writerClass
                      for name, writerClass in self._registered.items()
                      if writerClass.isAvailable()}
        self._dirty = False

    @cbook.deprecated("3.2")
    @property
    def avail(self):
        return {name: self._registered[name] for name in self.list()}

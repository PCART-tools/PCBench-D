    def replace(self, writer, factory):
        try:
            idx = self._waiters.index(writer)
            writer = factory(self, self._loop, False)
            self._waiters[idx] = writer
            return writer
        except ValueError:
            self.available = True
            return factory(self, self._loop)

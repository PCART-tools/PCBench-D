    def __call__(self):
        'Return the locations of the ticks'
        self.refresh()
        return self.raise_if_exceeds(self._locator())

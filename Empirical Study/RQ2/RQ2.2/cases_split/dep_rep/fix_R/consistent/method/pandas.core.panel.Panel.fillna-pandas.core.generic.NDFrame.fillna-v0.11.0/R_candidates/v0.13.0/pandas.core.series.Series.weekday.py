    @property
    def weekday(self):
        return self._constructor([d.weekday() for d in self.index],
                                 index=self.index).__finalize__(self)

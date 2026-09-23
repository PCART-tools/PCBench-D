    @Appender(Index.difference.__doc__)
    def difference(self, other, sort=None):
        new_idx = super().difference(other, sort=sort)
        new_idx._set_freq(None)
        return new_idx

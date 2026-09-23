    @Appender(Index.difference.__doc__)
    def difference(self, other, sort=None):
        new_idx = super().difference(other, sort=sort)._with_freq(None)
        return new_idx

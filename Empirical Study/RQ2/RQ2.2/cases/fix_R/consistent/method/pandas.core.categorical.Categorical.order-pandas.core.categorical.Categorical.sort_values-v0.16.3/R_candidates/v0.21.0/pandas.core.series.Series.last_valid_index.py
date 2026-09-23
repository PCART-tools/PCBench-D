    @Appender(generic._shared_docs['valid_index'] % {
        'position': 'last', 'klass': 'Series'})
    def last_valid_index(self):
        if len(self) == 0:
            return None

        mask = isna(self._values[::-1])
        i = mask.argmin()
        if mask[i]:
            return None
        else:
            return self.index[len(self) - i - 1]

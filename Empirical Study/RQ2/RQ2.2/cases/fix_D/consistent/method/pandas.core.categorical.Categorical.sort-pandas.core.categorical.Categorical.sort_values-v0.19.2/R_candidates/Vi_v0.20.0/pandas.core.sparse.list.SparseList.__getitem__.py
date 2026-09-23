    def __getitem__(self, i):
        if i < 0:
            if i + len(self) < 0:  # pragma: no cover
                raise ValueError('%d out of range' % i)
            i += len(self)

        passed = 0
        j = 0
        while i >= passed + len(self._chunks[j]):
            passed += len(self._chunks[j])
            j += 1
        return self._chunks[j][i - passed]

    @classmethod
    def _from_fastpath(cls, categories=None, ordered=False):
        self = cls.__new__(cls)
        self._finalize(categories, ordered, fastpath=True)
        return self

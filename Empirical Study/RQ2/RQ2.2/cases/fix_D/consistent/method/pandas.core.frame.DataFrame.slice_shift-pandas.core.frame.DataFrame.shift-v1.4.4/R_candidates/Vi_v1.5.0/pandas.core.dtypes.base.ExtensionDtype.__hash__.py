    def __hash__(self) -> int:
        # for python>=3.10, different nan objects have different hashes
        # we need  to avoid that und thus use hash function with old behavior
        return object_hash(tuple(getattr(self, attr) for attr in self._metadata))

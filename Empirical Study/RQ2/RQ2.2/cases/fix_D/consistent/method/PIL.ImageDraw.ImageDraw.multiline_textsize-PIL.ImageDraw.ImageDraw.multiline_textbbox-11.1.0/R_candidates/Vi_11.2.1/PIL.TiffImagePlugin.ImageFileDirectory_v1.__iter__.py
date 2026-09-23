    def __iter__(self) -> Iterator[int]:
        return iter(set(self._tagdata) | set(self._tags_v1))

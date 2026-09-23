    def __len__(self) -> int:
        return len(set(self._tagdata) | set(self._tags_v1))

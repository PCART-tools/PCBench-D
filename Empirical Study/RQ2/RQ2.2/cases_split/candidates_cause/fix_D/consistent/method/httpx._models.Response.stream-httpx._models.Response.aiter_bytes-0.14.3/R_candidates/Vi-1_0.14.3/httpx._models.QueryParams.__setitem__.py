    def __setitem__(self, key: str, value: str) -> None:
        self._dict[key] = value

        found_indexes = []
        for idx, (item_key, _) in enumerate(self._list):
            if item_key == key:
                found_indexes.append(idx)

        for idx in reversed(found_indexes[1:]):
            del self._list[idx]

        if found_indexes:
            idx = found_indexes[0]
            self._list[idx] = (key, value)
        else:
            self._list.append((key, value))

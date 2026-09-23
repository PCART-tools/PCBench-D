    def is_type_compatible(self, kind: str) -> bool:
        return kind in self._data._infer_matches

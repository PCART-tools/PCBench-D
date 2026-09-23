    def __contains__(self, tag: object) -> bool:
        return tag in self._tags_v2 or tag in self._tagdata

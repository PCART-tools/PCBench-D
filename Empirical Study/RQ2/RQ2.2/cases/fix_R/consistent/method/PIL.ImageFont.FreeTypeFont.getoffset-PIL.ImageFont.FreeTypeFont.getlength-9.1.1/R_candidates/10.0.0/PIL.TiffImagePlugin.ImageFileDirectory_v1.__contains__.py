    def __contains__(self, tag):
        return tag in self._tags_v1 or tag in self._tagdata

    def __setitem__(self, tag, value):
        for legacy_api in (False, True):
            self._setitem(tag, value, legacy_api)

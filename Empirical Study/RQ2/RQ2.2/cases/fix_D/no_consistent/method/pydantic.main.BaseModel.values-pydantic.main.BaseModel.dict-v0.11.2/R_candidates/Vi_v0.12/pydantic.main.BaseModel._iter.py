    def _iter(self, by_alias=False):
        for k, v in self.__values__.items():
            yield k, self._get_value(v, by_alias=by_alias)

    def to_pydatetime(self):
        return cast(ArrowExtensionArray, self._parent.array)._dt_to_pydatetime()

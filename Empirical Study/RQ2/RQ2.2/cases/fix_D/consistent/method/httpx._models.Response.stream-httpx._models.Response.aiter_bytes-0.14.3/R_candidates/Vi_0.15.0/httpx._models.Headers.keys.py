    def keys(self) -> typing.KeysView[str]:
        return {key.decode(self.encoding): None for key in self._dict.keys()}.keys()

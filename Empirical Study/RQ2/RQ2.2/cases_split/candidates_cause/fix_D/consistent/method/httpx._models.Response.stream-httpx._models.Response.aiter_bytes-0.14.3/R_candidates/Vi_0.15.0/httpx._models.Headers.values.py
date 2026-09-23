    def values(self) -> typing.ValuesView[str]:
        return {
            key: value.decode(self.encoding) for key, value in self._dict.items()
        }.values()

    def items(self) -> typing.ItemsView[str, str]:
        """
        Return `(key, value)` items of headers. Concatenate headers
        into a single comma seperated value when a key occurs multiple times.
        """
        return {
            key.decode(self.encoding): value.decode(self.encoding)
            for key, value in self._dict.items()
        }.items()

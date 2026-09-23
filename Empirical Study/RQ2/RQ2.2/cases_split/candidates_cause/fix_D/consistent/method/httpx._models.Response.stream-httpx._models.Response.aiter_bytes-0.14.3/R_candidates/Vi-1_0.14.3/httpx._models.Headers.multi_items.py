    def multi_items(self) -> typing.List[typing.Tuple[str, str]]:
        """
        Return a list of `(key, value)` pairs of headers. Allow multiple
        occurences of the same key without concatenating into a single
        comma seperated value.
        """
        return [
            (key.decode(self.encoding), value.decode(self.encoding))
            for key, value in self._list
        ]

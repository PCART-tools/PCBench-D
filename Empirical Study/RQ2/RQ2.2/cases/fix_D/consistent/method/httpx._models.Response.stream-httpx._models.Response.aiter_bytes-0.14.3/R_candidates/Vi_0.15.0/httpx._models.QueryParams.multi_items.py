    def multi_items(self) -> typing.List[typing.Tuple[str, str]]:
        """
        Return all items in the query params. Allow duplicate keys to occur.
        """
        return list(self._list)

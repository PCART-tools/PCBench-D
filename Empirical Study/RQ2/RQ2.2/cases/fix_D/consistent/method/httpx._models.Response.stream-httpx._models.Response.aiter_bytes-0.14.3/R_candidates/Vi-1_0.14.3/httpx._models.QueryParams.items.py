    def items(self) -> typing.ItemsView:
        """
        Return all items in the query params. If a key occurs more than once
        only the first item for that key is returned.
        """
        return self._dict.items()

    def get_list(self, key: typing.Any) -> typing.List[str]:
        """
        Get all values from the query param for a given key.
        """
        return [item_value for item_key, item_value in self._list if item_key == key]

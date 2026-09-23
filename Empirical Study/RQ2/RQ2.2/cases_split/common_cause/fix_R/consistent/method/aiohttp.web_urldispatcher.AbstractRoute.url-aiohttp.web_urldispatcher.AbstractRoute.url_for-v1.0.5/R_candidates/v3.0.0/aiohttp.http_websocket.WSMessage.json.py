    def json(self, *, loads=json.loads):
        """Return parsed JSON data.

        .. versionadded:: 0.22
        """
        return loads(self.data)

    def _dir_deletions(self):
        """
        Delete unwanted __dir__ for this object.
        """
        return self._accessors | self._deprecations

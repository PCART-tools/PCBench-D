    def _dir_deletions(self):
        """ delete unwanted __dir__ for this object """
        return self._accessors | self._deprecations

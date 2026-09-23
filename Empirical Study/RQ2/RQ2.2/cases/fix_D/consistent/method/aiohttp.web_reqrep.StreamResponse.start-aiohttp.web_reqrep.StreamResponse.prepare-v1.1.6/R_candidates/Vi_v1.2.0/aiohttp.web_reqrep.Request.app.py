    @reify
    def app(self):
        """Application instance."""
        return self._match_info.apps[-1]

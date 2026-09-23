    def url(self, **kwargs):
        """Construct url for route with additional params."""
        super().url(**kwargs)
        return self._resource.url(**kwargs)

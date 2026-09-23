    def url_for(self, *args, **kwargs):
        """Construct url for route with additional params."""
        return self._resource.url_for(*args, **kwargs)

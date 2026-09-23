    @abc.abstractmethod  # pragma: no branch
    def url_for(self, *args, **kwargs):
        """Construct url for route with additional params."""

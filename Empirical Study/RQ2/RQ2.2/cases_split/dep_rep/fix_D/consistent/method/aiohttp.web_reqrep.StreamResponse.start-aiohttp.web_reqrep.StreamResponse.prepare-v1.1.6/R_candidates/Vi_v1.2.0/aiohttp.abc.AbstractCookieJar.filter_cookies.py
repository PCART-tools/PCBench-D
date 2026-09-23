    @abstractmethod
    def filter_cookies(self, request_url):
        """Return the jar's cookies filtered by their attributes."""

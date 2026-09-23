    def url(self, **kwargs):
        """Construct url for route with additional params."""
        raise RuntimeError(".url() is not supported "
                           "by sub-application root")

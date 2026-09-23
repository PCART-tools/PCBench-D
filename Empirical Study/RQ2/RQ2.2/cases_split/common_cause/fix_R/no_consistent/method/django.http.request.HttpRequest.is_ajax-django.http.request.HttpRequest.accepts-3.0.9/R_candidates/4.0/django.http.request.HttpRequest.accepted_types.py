    @cached_property
    def accepted_types(self):
        """Return a list of MediaType instances."""
        return parse_accept_header(self.headers.get('Accept', '*/*'))

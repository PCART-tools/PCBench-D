    def append_form(self, obj, headers=None):
        """Helper to append form urlencoded part."""
        if not headers:
            headers = CIMultiDict()
        headers[CONTENT_TYPE] = 'application/x-www-form-urlencoded'
        assert isinstance(obj, (Sequence, Mapping))
        return self.append(obj, headers)

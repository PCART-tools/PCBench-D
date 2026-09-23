    def append_json(self, obj, headers=None):
        """Helper to append JSON part."""
        if not headers:
            headers = CIMultiDict()
        headers[CONTENT_TYPE] = 'application/json'
        return self.append(obj, headers)

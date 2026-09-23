    def append_form(self, obj, headers=None):
        """Helper to append form urlencoded part."""
        assert isinstance(obj, (Sequence, Mapping))

        if headers is None:
            headers = CIMultiDict()

        if isinstance(obj, Mapping):
            obj = list(obj.items())
        data = urlencode(obj, doseq=True)

        return self.append_payload(
            StringPayload(data, headers=headers,
                          content_type='application/x-www-form-urlencoded'))

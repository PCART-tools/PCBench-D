    def append_json(self, obj, headers=None):
        """Helper to append JSON part."""
        if headers is None:
            headers = CIMultiDict()

        data = json.dumps(obj).encode('utf-8')
        self.append_payload(
            BytesPayload(
                data, headers=headers, content_type='application/json'))

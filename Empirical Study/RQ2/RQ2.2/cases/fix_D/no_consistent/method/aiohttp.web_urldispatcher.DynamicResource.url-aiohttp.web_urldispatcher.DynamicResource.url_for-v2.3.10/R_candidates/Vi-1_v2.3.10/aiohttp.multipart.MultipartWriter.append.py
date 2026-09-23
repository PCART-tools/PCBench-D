    def append(self, obj, headers=None):
        if headers is None:
            headers = CIMultiDict()

        if isinstance(obj, Payload):
            if obj.headers is not None:
                obj.headers.update(headers)
            else:
                obj._headers = headers
            self.append_payload(obj)
        else:
            try:
                self.append_payload(get_payload(obj, headers=headers))
            except LookupError:
                raise TypeError

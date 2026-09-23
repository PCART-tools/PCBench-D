    def to_python(self, value):
        # If it's a string, it should be base64-encoded data
        if isinstance(value, six.text_type):
            return six.memoryview(b64decode(force_bytes(value)))
        return value

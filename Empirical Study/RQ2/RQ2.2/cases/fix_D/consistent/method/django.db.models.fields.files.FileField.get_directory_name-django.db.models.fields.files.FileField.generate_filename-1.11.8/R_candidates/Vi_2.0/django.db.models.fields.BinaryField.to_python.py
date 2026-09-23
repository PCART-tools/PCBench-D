    def to_python(self, value):
        # If it's a string, it should be base64-encoded data
        if isinstance(value, str):
            return memoryview(b64decode(force_bytes(value)))
        return value

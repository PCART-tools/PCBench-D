    def _set_streaming_content(self, value):
        # Ensure we can never iterate on "value" more than once.
        self._iterator = iter(value)
        if hasattr(value, 'close'):
            self._resource_closers.append(value.close)

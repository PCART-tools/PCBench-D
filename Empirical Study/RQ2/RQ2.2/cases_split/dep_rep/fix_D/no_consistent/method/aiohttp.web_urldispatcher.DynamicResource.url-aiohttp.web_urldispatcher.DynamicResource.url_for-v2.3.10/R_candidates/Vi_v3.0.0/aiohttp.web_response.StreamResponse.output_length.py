    @property
    def output_length(self):
        warnings.warn('output_length is deprecated', DeprecationWarning)
        return self._payload_writer.buffer_size

    def _check_buffer_size(self):
        if self._stream.paused:
            if self._buffer_size < self._b_limit:
                try:
                    self._stream.transport.resume_reading()
                except (AttributeError, NotImplementedError):
                    pass
                else:
                    self._stream.paused = False
        else:
            if self._buffer_size > self._b_limit:
                try:
                    self._stream.transport.pause_reading()
                except (AttributeError, NotImplementedError):
                    pass
                else:
                    self._stream.paused = True

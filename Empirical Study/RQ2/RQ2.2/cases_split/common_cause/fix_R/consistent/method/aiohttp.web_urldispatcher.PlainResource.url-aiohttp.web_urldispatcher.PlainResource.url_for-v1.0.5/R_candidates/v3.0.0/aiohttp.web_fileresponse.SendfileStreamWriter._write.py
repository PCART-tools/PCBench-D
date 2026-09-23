    def _write(self, chunk):
        # we overwrite StreamWriter._write, so nothing can be appended to
        # _buffer, and nothing is written to the transport directly by the
        # parent class
        self.output_size += len(chunk)
        self._sendfile_buffer.append(chunk)

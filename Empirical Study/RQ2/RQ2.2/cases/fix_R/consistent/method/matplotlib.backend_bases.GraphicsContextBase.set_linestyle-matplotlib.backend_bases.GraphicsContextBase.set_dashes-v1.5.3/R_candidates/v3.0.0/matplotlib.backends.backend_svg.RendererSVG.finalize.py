    def finalize(self):
        self._write_clips()
        self._write_hatches()
        self._write_svgfonts()
        self.writer.close(self._start_id)
        self.writer.flush()

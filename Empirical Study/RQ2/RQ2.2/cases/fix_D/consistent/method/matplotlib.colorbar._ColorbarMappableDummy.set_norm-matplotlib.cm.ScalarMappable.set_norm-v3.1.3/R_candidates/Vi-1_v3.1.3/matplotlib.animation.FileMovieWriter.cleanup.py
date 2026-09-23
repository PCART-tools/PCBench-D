    def cleanup(self):
        MovieWriter.cleanup(self)

        # Delete temporary files
        if self.clear_temp:
            _log.debug('MovieWriter: clearing temporary fnames=%s',
                       self._temp_names)
            for fname in self._temp_names:
                os.remove(fname)

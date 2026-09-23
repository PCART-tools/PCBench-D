    def cleanup(self):
        MovieWriter.cleanup(self)

        # Delete temporary files
        if self.clear_temp:
            _log.debug('MovieWriter: clearing temporary paths=%s',
                       self._temp_paths)
            for path in self._temp_paths:
                path.unlink()

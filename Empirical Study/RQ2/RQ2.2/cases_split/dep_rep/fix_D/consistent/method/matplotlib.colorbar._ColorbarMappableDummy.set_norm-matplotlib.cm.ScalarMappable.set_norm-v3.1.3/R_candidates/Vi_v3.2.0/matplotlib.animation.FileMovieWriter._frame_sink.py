    def _frame_sink(self):
        # Creates a filename for saving using the basename and the current
        # counter.
        path = Path(self._base_temp_name() % self._frame_counter)

        # Save the filename so we can delete it later if necessary
        self._temp_paths.append(path)
        _log.debug('FileMovieWriter.frame_sink: saving frame %d to path=%s',
                   self._frame_counter, path)
        self._frame_counter += 1  # Ensures each created name is 'unique'

        # This file returned here will be closed once it's used by savefig()
        # because it will no longer be referenced and will be gc-ed.
        return open(path, 'wb')

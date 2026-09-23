    def finish(self):
        # Call run here now that all frame grabbing is done. All temp files
        # are available to be assembled.
        self._run()
        MovieWriter.finish(self)  # Will call clean-up

        # Check error code for creating file here, since we just run
        # the process here, rather than having an open pipe.
        if self._proc.returncode:
            try:
                stdout = [s.decode() for s in self._proc._stdout_buff]
                stderr = [s.decode() for s in self._proc._stderr_buff]
                _log.info("MovieWriter.finish: stdout: %s", stdout)
                _log.info("MovieWriter.finish: stderr: %s", stderr)
            except Exception as e:
                pass
            raise RuntimeError('Error creating movie, return code: {}'
                               .format(self._proc.returncode))

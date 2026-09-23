    def finish(self):
        """Finish any processing for writing the movie."""
        out, err = self._proc.communicate()
        # Use the encoding/errors that universal_newlines would use.
        out = TextIOWrapper(BytesIO(out)).read()
        err = TextIOWrapper(BytesIO(err)).read()
        if out:
            _log.log(
                logging.WARNING if self._proc.returncode else logging.DEBUG,
                "MovieWriter stdout:\n%s", out)
        if err:
            _log.log(
                logging.WARNING if self._proc.returncode else logging.DEBUG,
                "MovieWriter stderr:\n%s", err)
        if self._proc.returncode:
            raise subprocess.CalledProcessError(
                self._proc.returncode, self._proc.args, out, err)

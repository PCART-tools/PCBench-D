    def _run(self):
        # Uses subprocess to call the program for assembling frames into a
        # movie file.  *args* returns the sequence of command line arguments
        # from a few configuration options.
        command = self._args()
        _log.info('MovieWriter.run: running command: %s', command)
        PIPE = subprocess.PIPE
        self._proc = subprocess.Popen(
            command, stdin=PIPE, stdout=PIPE, stderr=PIPE,
            creationflags=subprocess_creation_flags)

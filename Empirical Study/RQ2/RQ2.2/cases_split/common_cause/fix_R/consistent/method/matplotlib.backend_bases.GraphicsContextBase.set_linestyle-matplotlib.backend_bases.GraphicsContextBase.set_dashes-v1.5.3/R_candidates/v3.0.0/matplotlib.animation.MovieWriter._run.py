    def _run(self):
        # Uses subprocess to call the program for assembling frames into a
        # movie file.  *args* returns the sequence of command line arguments
        # from a few configuration options.
        command = self._args()
        output = subprocess.PIPE
        _log.info('MovieWriter.run: running command: %s', command)
        self._proc = subprocess.Popen(command, shell=False,
                                      stdout=output, stderr=output,
                                      stdin=subprocess.PIPE,
                                      creationflags=subprocess_creation_flags)

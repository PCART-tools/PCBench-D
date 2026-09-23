    def _run(self):
        # Uses subprocess to call the program for assembling frames into a
        # movie file.  *args* returns the sequence of command line arguments
        # from a few configuration options.
        command = self._args()
        if verbose.ge('debug'):
            output = sys.stdout
        else:
            output = subprocess.PIPE
        verbose.report('MovieWriter.run: running command: %s' %
                       ' '.join(command))
        self._proc = subprocess.Popen(command, shell=False,
                                      stdout=output, stderr=output,
                                      stdin=subprocess.PIPE,
                                      creationflags=subprocess_creation_flags)

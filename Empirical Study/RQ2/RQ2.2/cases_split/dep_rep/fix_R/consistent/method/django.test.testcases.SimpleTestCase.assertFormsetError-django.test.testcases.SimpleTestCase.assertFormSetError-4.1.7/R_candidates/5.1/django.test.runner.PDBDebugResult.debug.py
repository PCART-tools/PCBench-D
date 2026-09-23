    def debug(self, error):
        self._restoreStdout()
        self.buffer = False
        exc_type, exc_value, traceback = error
        print("\nOpening PDB: %r" % exc_value)
        pdb.post_mortem(traceback)

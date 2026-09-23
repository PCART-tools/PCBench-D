    def _cleanup(self):
        if not self._os_path.isdir(self.tmpdir):
            return
        try:
            self.latex.communicate()
            self.latex_stdin_utf8.close()
            self.latex.stdout.close()
        except:
            pass
        try:
            self._shutil.rmtree(self.tmpdir)
            LatexManager._unclean_instances.discard(self)
        except:
            sys.stderr.write("error deleting tmp directory %s\n" % self.tmpdir)

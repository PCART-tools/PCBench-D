    def close(self):
        """
        Finalize this object, running LaTeX in a temporary directory
        and moving the final pdf file to *filename*.
        """
        self._file.write(rb'\end{document}\n')
        self._file.close()

        if self._n_figures > 0:
            try:
                self._run_latex()
            finally:
                try:
                    shutil.rmtree(self._tmpdir)
                except:
                    TmpDirCleaner.add(self._tmpdir)
        elif self.keep_empty:
            open(self._outputfile, 'wb').close()

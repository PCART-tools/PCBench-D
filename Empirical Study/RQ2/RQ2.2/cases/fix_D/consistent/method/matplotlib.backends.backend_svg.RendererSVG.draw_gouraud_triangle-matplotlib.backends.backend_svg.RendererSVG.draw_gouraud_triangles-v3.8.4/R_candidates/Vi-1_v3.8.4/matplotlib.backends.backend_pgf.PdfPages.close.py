    def close(self):
        """
        Finalize this object, running LaTeX in a temporary directory
        and moving the final pdf file to *filename*.
        """
        self._file.write(rb'\end{document}\n')
        if self._n_figures > 0:
            self._run_latex()
        elif self._keep_empty:
            _api.warn_deprecated("3.8", message=(
                "Keeping empty pdf files is deprecated since %(since)s and support "
                "will be removed %(removal)s."))
            open(self._output_name, 'wb').close()
        self._file.close()

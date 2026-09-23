    def print_pdf(self, fname_or_fh, *args, **kwargs):
        """Use LaTeX to compile a Pgf generated figure to PDF."""
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return
        with cbook.open_file_cm(fname_or_fh, "wb") as file:
            self._print_pdf_to_fh(file, *args, **kwargs)

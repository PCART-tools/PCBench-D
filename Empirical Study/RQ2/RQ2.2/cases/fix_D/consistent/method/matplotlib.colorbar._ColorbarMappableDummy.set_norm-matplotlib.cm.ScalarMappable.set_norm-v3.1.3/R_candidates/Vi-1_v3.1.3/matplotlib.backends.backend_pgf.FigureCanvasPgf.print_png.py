    def print_png(self, fname_or_fh, *args, **kwargs):
        """Use LaTeX to compile a pgf figure to pdf and convert it to png."""
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return
        with cbook.open_file_cm(fname_or_fh, "wb") as file:
            self._print_png_to_fh(file, *args, **kwargs)

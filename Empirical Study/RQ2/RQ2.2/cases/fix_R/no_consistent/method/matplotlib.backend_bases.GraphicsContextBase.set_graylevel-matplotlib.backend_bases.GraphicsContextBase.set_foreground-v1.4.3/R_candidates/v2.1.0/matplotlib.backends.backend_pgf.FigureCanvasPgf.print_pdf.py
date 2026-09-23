    def print_pdf(self, fname_or_fh, *args, **kwargs):
        """
        Use LaTeX to compile a Pgf generated figure to PDF.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        # figure out where the pdf is to be written to
        if isinstance(fname_or_fh, six.string_types):
            with open(fname_or_fh, "wb") as fh:
                self._print_pdf_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            self._print_pdf_to_fh(fname_or_fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path or a file-like object")

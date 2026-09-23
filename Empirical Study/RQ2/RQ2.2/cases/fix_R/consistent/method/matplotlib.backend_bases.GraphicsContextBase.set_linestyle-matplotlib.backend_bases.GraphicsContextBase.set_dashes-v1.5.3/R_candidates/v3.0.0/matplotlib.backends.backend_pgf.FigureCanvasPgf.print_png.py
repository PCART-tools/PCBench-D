    def print_png(self, fname_or_fh, *args, **kwargs):
        """
        Use LaTeX to compile a pgf figure to pdf and convert it to png.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        if isinstance(fname_or_fh, str):
            with open(fname_or_fh, "wb") as fh:
                self._print_png_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            self._print_png_to_fh(fname_or_fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path or a file-like object")

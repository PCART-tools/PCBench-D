    def print_pgf(self, fname_or_fh, *args, **kwargs):
        """
        Output pgf commands for drawing the figure so it can be included and
        rendered in latex documents.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return

        # figure out where the pgf is to be written to
        if isinstance(fname_or_fh, str):
            with open(fname_or_fh, "w", encoding="utf-8") as fh:
                self._print_pgf_to_fh(fh, *args, **kwargs)
        elif is_writable_file_like(fname_or_fh):
            fh = codecs.getwriter("utf-8")(fname_or_fh)
            self._print_pgf_to_fh(fh, *args, **kwargs)
        else:
            raise ValueError("filename must be a path")

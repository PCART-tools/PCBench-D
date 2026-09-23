    def print_pgf(self, fname_or_fh, *args, **kwargs):
        """
        Output pgf macros for drawing the figure so it can be included and
        rendered in latex documents.
        """
        if kwargs.get("dryrun", False):
            self._print_pgf_to_fh(None, *args, **kwargs)
            return
        with cbook.open_file_cm(fname_or_fh, "w", encoding="utf-8") as file:
            if not cbook.file_requires_unicode(file):
                file = codecs.getwriter("utf-8")(file)
            self._print_pgf_to_fh(file, *args, **kwargs)

    def print_svg(self, filename, *args, **kwargs):
        with cbook.open_file_cm(filename, "w", encoding="utf-8") as fh:

            filename = getattr(fh, 'name', '')
            if not isinstance(filename, str):
                filename = ''

            if cbook.file_requires_unicode(fh):
                detach = False
            else:
                fh = io.TextIOWrapper(fh, 'utf-8')
                detach = True

            result = self._print_svg(filename, fh, **kwargs)

            # Detach underlying stream from wrapper so that it remains open in
            # the caller.
            if detach:
                fh.detach()

        return result

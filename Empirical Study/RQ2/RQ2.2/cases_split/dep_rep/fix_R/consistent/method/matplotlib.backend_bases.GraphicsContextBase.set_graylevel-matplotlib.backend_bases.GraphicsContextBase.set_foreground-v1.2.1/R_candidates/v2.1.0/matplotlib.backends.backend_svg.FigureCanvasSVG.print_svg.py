    def print_svg(self, filename, *args, **kwargs):
        if isinstance(filename, six.string_types):
            with io.open(filename, 'w', encoding='utf-8') as svgwriter:
                return self._print_svg(filename, svgwriter, **kwargs)

        if not is_writable_file_like(filename):
            raise ValueError("filename must be a path or a file-like object")

        svgwriter = filename
        filename = getattr(svgwriter, 'name', '')
        if not isinstance(filename, six.string_types):
            filename = ''

        if not isinstance(svgwriter, io.TextIOBase):
            if six.PY3:
                svgwriter = io.TextIOWrapper(svgwriter, 'utf-8')
            else:
                svgwriter = codecs.getwriter('utf-8')(svgwriter)
            detach = True
        else:
            detach = False

        result = self._print_svg(filename, svgwriter, **kwargs)

        # Detach underlying stream from wrapper so that it remains open in the
        # caller.
        if detach:
            if six.PY3:
                svgwriter.detach()
            else:
                svgwriter.reset()
                svgwriter.stream = io.BytesIO()

        return result

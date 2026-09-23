    def _format_with_header(self, header, **kwargs):
        return header + list(self._format_native_types(**kwargs))

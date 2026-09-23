    def _format_with_header(self, header, na_rep="NaT", **kwargs):
        return header + list(self._format_native_types(na_rep, **kwargs))

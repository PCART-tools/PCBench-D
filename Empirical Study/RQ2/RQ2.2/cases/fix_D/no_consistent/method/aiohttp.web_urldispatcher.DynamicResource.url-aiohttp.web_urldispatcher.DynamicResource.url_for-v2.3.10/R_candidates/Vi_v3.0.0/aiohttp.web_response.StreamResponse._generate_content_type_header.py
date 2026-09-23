    def _generate_content_type_header(self, CONTENT_TYPE=hdrs.CONTENT_TYPE):
        params = '; '.join("%s=%s" % i for i in self._content_dict.items())
        if params:
            ctype = self._content_type + '; ' + params
        else:
            ctype = self._content_type
        self.headers[CONTENT_TYPE] = ctype

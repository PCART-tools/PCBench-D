    def _add_default_headers(self):
        super()._add_default_headers()

        if hdrs.DATE not in self.headers:
            # format_date_time(None) is quite expensive
            self.headers.setdefault(hdrs.DATE, format_date_time(None))
        self.headers.setdefault(hdrs.SERVER, self.SERVER_SOFTWARE)

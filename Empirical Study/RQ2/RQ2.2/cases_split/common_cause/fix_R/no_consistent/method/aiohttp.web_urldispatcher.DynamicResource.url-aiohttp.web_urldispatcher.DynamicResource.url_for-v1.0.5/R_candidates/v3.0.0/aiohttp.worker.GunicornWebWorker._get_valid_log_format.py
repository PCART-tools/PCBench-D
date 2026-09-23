    def _get_valid_log_format(self, source_format):
        if source_format == self.DEFAULT_GUNICORN_LOG_FORMAT:
            return self.DEFAULT_AIOHTTP_LOG_FORMAT
        elif re.search(r'%\([^\)]+\)', source_format):
            raise ValueError(
                "Gunicorn's style options in form of `%(name)s` are not "
                "supported for the log formatting. Please use aiohttp's "
                "format specification to configure access log formatting: "
                "http://docs.aiohttp.org/en/stable/logging.html"
                "#format-specification"
            )
        else:
            return source_format

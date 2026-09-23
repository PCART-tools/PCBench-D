    def url_for(self, **parts):
        url = self._formatter.format_map(parts)
        return URL(url)

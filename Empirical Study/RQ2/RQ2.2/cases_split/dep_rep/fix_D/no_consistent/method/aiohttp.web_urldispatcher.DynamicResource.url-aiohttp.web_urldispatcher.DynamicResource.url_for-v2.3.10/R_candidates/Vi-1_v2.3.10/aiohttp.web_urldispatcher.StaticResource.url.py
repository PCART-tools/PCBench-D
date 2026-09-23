    def url(self, *, filename, append_version=None, query=None):
        url = self.url_for(filename=filename, append_version=append_version)
        if query is not None:
            return str(url.update_query(query))
        return str(url)

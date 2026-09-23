    def url(self, *, filename, query=None):
        return str(self.url_for(filename=filename).with_query(query))

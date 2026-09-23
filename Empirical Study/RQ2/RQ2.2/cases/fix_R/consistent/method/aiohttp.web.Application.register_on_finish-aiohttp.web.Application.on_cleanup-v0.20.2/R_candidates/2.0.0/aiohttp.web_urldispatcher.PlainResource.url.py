    def url(self, *, query=None):
        super().url()
        return str(self.url_for().with_query(query))

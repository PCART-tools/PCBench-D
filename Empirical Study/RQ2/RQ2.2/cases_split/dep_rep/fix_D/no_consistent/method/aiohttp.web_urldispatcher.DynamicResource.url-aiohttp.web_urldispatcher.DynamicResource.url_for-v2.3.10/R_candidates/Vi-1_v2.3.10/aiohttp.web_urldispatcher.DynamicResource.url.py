    def url(self, *, parts, query=None):
        super().url(**parts)
        return str(self.url_for(**parts).with_query(query))

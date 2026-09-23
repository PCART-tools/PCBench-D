    def url_for(self):
        return URL.build(path=self._path, encoded=True)

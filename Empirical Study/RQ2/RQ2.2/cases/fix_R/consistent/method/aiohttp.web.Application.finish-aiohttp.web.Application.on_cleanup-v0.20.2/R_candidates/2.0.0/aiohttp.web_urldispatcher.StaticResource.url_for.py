    def url_for(self, *, filename):
        if isinstance(filename, Path):
            filename = str(filename)
        while filename.startswith('/'):
            filename = filename[1:]
        filename = '/' + filename
        url = self._prefix + URL(filename).raw_path
        return URL(url)

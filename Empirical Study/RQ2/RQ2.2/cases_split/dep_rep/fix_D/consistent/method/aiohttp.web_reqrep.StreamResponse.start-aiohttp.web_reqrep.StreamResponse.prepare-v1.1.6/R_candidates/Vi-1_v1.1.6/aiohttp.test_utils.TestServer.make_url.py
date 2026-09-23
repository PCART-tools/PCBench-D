    def make_url(self, path):
        url = URL(path)
        assert not url.is_absolute()
        return self._root.join(url)

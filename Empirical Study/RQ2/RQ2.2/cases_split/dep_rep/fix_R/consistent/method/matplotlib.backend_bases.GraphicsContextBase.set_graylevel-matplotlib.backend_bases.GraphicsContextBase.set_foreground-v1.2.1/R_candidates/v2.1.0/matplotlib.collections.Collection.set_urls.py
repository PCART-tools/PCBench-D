    def set_urls(self, urls):
        if urls is None:
            self._urls = [None, ]
        else:
            self._urls = urls
        self.stale = True

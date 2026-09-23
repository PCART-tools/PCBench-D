    def set_urls(self, urls):
        """
        Parameters
        ----------
        urls : List[str] or None
        """
        self._urls = urls if urls is not None else [None]
        self.stale = True

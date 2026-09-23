    def url_for(self, **parts):
        url = self._formatter.format_map({k: URL.build(path=v).raw_path
                                          for k, v in parts.items()})
        return URL.build(path=url)

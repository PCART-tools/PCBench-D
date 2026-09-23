    def _match(self, path):
        match = self._pattern.fullmatch(path)
        if match is None:
            return None
        else:
            return {key: URL.build(path=value, encoded=True).path
                    for key, value in
                    match.groupdict().items()}

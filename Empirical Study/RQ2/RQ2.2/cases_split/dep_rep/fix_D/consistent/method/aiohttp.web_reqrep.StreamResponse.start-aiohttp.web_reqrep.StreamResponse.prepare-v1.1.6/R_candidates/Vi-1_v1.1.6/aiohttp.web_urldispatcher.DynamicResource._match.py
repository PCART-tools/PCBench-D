    def _match(self, path):
        match = self._pattern.fullmatch(path)
        if match is None:
            return None
        else:
            return {key: unquote(value) for key, value in
                    match.groupdict().items()}

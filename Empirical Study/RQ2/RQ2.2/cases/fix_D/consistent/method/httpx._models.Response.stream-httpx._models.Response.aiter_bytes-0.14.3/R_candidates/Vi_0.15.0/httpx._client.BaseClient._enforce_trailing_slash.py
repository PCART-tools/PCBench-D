    def _enforce_trailing_slash(self, url: URL) -> URL:
        if url.path.endswith("/"):
            return url
        return url.copy_with(path=url.path + "/")

    def clone(self, *, method=sentinel, rel_url=sentinel,
              headers=sentinel, scheme=sentinel, host=sentinel,
              remote=sentinel):
        ret = super().clone(method=method,
                            rel_url=rel_url,
                            headers=headers,
                            scheme=scheme,
                            host=host,
                            remote=remote)
        ret._match_info = self._match_info
        return ret

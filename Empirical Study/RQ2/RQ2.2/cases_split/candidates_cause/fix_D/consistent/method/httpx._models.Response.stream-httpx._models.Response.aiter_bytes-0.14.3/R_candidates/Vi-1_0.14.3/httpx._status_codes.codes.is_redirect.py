    @classmethod
    def is_redirect(cls, value: int) -> bool:
        return value in (
            # 301 (Cacheable redirect. Method may change to GET.)
            codes.MOVED_PERMANENTLY,
            # 302 (Uncacheable redirect. Method may change to GET.)
            codes.FOUND,
            # 303 (Client should make a GET or HEAD request.)
            codes.SEE_OTHER,
            # 307 (Equiv. 302, but retain method)
            codes.TEMPORARY_REDIRECT,
            # 308 (Equiv. 301, but retain method)
            codes.PERMANENT_REDIRECT,
        )

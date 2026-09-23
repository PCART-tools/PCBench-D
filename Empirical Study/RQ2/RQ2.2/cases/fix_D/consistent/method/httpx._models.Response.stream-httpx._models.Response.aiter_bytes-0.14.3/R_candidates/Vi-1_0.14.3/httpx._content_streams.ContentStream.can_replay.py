    def can_replay(self) -> bool:
        """
        Return `True` if `__aiter__` can be called multiple times.

        We need this in cases such determining if we can re-issue a request
        body when we receive a redirect response.
        """
        return True

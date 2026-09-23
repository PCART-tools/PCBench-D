    def next(self) -> "Response":
        """
        Get the next response from a redirect response.
        """
        if not self.is_redirect:
            message = (
                "Called .next(), but the response was not a redirect. "
                "Calling code should check `response.is_redirect` first."
            )
            raise NotRedirectResponse(message)
        assert self.call_next is not None
        return self.call_next()

    async def anext(self) -> "Response":
        """
        Get the next response from a redirect response.
        """
        if not self.is_redirect:
            raise NotRedirectResponse(
                "Called .anext(), but the response was not a redirect. "
                "Calling code should check `response.is_redirect` first."
            )
        assert self.call_next is not None
        return await self.call_next()

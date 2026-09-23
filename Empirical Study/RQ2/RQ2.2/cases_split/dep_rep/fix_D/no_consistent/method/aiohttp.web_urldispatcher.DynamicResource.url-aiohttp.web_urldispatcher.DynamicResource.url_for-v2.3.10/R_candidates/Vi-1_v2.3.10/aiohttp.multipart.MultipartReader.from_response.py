    @classmethod
    def from_response(cls, response):
        """Constructs reader instance from HTTP response.

        :param response: :class:`~aiohttp.client.ClientResponse` instance
        """
        obj = cls.response_wrapper_cls(response, cls(response.headers,
                                                     response.content))
        return obj

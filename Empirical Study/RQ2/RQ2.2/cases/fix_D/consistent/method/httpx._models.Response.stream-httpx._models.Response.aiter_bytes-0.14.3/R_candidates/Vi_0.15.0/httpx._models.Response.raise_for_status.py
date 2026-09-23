    def raise_for_status(self) -> None:
        """
        Raise the `HTTPStatusError` if one occurred.
        """
        message = (
            "{0.status_code} {error_type}: {0.reason_phrase} for url: {0.url}\n"
            "For more information check: https://httpstatuses.com/{0.status_code}"
        )

        request = self._request
        if request is None:
            raise RuntimeError(
                "Cannot call `raise_for_status` as the request "
                "instance has not been set on this response."
            )

        if codes.is_client_error(self.status_code):
            message = message.format(self, error_type="Client Error")
            raise HTTPStatusError(message, request=request, response=self)
        elif codes.is_server_error(self.status_code):
            message = message.format(self, error_type="Server Error")
            raise HTTPStatusError(message, request=request, response=self)

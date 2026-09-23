    @property
    def stream(self):  # type: ignore
        warn_deprecated(  # pragma: nocover
            "Response.stream() is due to be deprecated. "
            "Use Response.aiter_bytes() instead.",
        )
        return self.aiter_bytes  # pragma: nocover

    def __del__(self) -> None:
        if not self.is_closed:
            warnings.warn(
                f"Unclosed {self!r}. "
                "See https://www.python-httpx.org/async/#opening-and-closing-clients "
                "for details."
            )

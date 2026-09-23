        def render_data(self) -> bytes:
            if not hasattr(self, "_data"):
                self._data = (
                    self.value
                    if isinstance(self.value, bytes)
                    else self.value.encode("utf-8")
                )

            return self._data

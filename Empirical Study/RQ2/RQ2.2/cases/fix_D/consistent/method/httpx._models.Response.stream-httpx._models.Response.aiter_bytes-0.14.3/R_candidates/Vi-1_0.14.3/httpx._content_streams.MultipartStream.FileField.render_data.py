        def render_data(self) -> typing.Iterator[bytes]:
            if isinstance(self.file, (str, bytes)):
                yield to_bytes(self.file)
                return

            if hasattr(self, "_data"):
                # Already rendered.
                yield self._data
                return

            for chunk in self.file:
                yield to_bytes(chunk)

            # Get ready for the next replay, if possible.
            if self.can_replay():
                assert self.file.seekable()
                self.file.seek(0)

    def flush(self) -> str:
        try:
            if self.decoder is None:
                # Empty string case as chardet is guaranteed to not have a guess.
                assert self.buffer is not None
                if len(self.buffer) == 0:
                    return ""
                return bytes(self.buffer).decode(self._detector_result())

            return self.decoder.decode(b"", True)
        except UnicodeDecodeError as exc:  # pragma: nocover
            raise ValueError(str(exc))

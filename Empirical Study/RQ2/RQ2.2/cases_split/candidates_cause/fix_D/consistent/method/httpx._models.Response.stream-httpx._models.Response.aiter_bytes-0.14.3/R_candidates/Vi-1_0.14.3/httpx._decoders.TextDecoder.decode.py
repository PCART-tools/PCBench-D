    def decode(self, data: bytes) -> str:
        try:
            if self.decoder is not None:
                text = self.decoder.decode(data)
            else:
                assert self.buffer is not None
                text = ""
                self.detector.feed(data)
                self.buffer += data

                # Should be more than enough data to process, we don't
                # want to buffer too long as chardet will wait until
                # detector.close() is used to give back common
                # encodings like 'utf-8'.
                if len(self.buffer) >= 4096:
                    self.decoder = codecs.getincrementaldecoder(
                        self._detector_result()
                    )()
                    text = self.decoder.decode(bytes(self.buffer), False)
                    self.buffer = None

            return text
        except UnicodeDecodeError as exc:  # pragma: nocover
            raise ValueError(str(exc))

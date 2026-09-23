    def iter_lines(self) -> typing.Iterator[str]:
        decoder = LineDecoder()
        with self._wrap_decoder_errors():
            for text in self.iter_text():
                for line in decoder.decode(text):
                    yield line
            for line in decoder.flush():
                yield line

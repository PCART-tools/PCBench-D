    async def aiter_lines(self) -> typing.AsyncIterator[str]:
        decoder = LineDecoder()
        with self._wrap_decoder_errors():
            async for text in self.aiter_text():
                for line in decoder.decode(text):
                    yield line
            for line in decoder.flush():
                yield line

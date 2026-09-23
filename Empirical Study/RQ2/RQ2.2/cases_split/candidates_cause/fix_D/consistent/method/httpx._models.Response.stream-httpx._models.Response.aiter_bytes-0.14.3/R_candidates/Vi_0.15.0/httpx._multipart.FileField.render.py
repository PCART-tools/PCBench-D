    def render(self) -> typing.Iterator[bytes]:
        yield self.render_headers()
        yield from self.render_data()

        def render(self) -> typing.Iterator[bytes]:
            yield self.render_headers()
            yield self.render_data()

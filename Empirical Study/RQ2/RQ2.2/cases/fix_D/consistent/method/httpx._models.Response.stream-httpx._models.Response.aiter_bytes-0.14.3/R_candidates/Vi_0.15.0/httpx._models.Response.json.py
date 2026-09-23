    def json(self, **kwargs: typing.Any) -> typing.Any:
        if self.charset_encoding is None and self.content and len(self.content) > 3:
            encoding = guess_json_utf(self.content)
            if encoding is not None:
                try:
                    return jsonlib.loads(self.content.decode(encoding), **kwargs)
                except UnicodeDecodeError:
                    pass
        return jsonlib.loads(self.text, **kwargs)

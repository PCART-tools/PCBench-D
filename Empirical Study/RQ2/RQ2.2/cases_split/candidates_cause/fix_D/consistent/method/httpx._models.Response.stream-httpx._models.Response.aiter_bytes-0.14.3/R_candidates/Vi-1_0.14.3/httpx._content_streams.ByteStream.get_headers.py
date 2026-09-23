    def get_headers(self) -> typing.Dict[str, str]:
        if not self.body:
            return {}
        content_length = str(len(self.body))
        return {"Content-Length": content_length}

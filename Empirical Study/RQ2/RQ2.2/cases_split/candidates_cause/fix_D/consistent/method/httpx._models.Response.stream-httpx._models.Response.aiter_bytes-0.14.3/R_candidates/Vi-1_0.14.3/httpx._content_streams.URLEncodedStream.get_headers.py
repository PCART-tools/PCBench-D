    def get_headers(self) -> typing.Dict[str, str]:
        content_length = str(len(self.body))
        content_type = "application/x-www-form-urlencoded"
        return {"Content-Length": content_length, "Content-Type": content_type}

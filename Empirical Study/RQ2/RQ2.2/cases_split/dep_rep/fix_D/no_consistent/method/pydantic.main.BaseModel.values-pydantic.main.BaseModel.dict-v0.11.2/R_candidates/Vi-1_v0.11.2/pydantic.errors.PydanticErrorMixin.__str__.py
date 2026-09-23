    def __str__(self) -> str:
        return self.msg_template.format(**self.ctx or {})

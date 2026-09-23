    def __init__(self, exc, *, loc, config=None):
        self.exc = exc
        self.loc = loc if isinstance(loc, tuple) else (loc,)
        self.msg_template = config.error_msg_templates.get(self.type_) if config else None

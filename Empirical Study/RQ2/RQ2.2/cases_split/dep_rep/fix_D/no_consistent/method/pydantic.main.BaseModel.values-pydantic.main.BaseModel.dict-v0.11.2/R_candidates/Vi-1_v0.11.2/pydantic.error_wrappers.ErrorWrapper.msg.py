    @property
    def msg(self):
        default_msg_template = getattr(self.exc, 'msg_template', None)
        msg_template = self.msg_template or default_msg_template
        if msg_template:
            return msg_template.format(**self.ctx or {})

        return str(self.exc)

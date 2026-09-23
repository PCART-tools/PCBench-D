    def __init__(self, method, allowed_methods, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        allow = ','.join(sorted(allowed_methods))
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Allow'] = allow
        self.allowed_methods = allowed_methods
        self.method = method.upper()

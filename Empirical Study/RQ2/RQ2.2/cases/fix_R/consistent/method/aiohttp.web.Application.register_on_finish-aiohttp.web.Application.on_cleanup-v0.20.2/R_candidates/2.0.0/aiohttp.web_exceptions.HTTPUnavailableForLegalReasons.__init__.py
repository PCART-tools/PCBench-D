    def __init__(self, link, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Link'] = '<%s>; rel="blocked-by"' % link
        self.link = link

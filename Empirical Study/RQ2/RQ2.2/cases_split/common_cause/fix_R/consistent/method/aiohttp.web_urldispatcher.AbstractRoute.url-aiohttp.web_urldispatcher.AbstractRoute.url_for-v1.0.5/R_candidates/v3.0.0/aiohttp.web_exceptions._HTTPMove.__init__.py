    def __init__(self, location, *, headers=None, reason=None,
                 body=None, text=None, content_type=None):
        if not location:
            raise ValueError("HTTP redirects need a location to redirect to.")
        super().__init__(headers=headers, reason=reason,
                         body=body, text=text, content_type=content_type)
        self.headers['Location'] = str(location)
        self.location = location

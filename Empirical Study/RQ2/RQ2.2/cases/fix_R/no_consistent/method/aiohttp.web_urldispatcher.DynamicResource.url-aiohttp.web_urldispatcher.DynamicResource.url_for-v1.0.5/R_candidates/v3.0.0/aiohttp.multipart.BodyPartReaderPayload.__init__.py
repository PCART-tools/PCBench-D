    def __init__(self, value, *args, **kwargs):
        super().__init__(value, *args, **kwargs)

        params = {}
        if value.name is not None:
            params['name'] = value.name
        if value.filename is not None:
            params['filename'] = value.name

        if params:
            self.set_content_disposition('attachment', **params)

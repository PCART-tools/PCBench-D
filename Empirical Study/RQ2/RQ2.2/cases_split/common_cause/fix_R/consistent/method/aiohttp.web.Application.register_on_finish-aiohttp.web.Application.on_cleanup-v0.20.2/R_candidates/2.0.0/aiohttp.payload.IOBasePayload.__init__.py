    def __init__(self, value, *args, **kwargs):
        if 'filename' not in kwargs:
            kwargs['filename'] = guess_filename(value)

        super().__init__(value, *args, **kwargs)

        if self._filename is not None:
            self.set_content_disposition('attachment', filename=self._filename)

    def __init__(self, value, disposition='attachment', *args, **kwargs):
        if 'filename' not in kwargs:
            kwargs['filename'] = guess_filename(value)

        super().__init__(value, *args, **kwargs)

        if self._filename is not None and disposition is not None:
            self.set_content_disposition(disposition, filename=self._filename)

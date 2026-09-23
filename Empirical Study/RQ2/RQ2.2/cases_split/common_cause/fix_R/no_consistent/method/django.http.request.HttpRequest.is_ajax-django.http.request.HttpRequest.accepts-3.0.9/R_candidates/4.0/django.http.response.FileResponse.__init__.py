    def __init__(self, *args, as_attachment=False, filename='', **kwargs):
        self.as_attachment = as_attachment
        self.filename = filename
        super().__init__(*args, **kwargs)

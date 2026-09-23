    def __init__(self, fields=(), quote_fields=True, charset=None):
        self._writer = multipart.MultipartWriter('form-data')
        self._fields = []
        self._is_multipart = False
        self._quote_fields = quote_fields
        self._charset = charset

        if isinstance(fields, dict):
            fields = list(fields.items())
        elif not isinstance(fields, (list, tuple)):
            fields = (fields,)
        self.add_fields(*fields)

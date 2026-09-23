    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super(NullBooleanField, self).__init__(*args, **kwargs)

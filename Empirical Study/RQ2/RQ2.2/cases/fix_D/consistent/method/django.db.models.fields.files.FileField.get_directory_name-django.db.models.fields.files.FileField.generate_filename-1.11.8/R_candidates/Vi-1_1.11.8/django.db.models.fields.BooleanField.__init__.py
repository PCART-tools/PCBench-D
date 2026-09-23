    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super(BooleanField, self).__init__(*args, **kwargs)

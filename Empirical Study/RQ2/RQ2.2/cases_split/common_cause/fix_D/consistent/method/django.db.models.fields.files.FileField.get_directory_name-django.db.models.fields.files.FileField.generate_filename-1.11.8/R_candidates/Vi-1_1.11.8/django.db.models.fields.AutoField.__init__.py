    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        super(AutoField, self).__init__(*args, **kwargs)

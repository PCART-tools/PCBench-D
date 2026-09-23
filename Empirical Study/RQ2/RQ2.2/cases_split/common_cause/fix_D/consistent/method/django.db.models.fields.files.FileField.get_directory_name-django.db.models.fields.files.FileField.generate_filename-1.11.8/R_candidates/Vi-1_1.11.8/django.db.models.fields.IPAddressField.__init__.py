    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 15
        super(IPAddressField, self).__init__(*args, **kwargs)

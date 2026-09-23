    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        super(URLField, self).__init__(verbose_name, name, **kwargs)

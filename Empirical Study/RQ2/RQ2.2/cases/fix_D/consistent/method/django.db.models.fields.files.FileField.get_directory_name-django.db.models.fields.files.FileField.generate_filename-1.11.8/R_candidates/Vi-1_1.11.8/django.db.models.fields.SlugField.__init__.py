    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        self.allow_unicode = kwargs.pop('allow_unicode', False)
        if self.allow_unicode:
            self.default_validators = [validators.validate_unicode_slug]
        super(SlugField, self).__init__(*args, **kwargs)

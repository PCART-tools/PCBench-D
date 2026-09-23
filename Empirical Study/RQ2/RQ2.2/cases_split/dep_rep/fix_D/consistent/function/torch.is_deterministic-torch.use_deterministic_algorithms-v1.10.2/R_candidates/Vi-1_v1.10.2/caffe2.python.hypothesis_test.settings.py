    def settings(**kwargs):
        if 'deadline' in kwargs:
            kwargs['deadline'] = None
            kwargs.setdefault('max_examples', 50)

        def wrapped(f):
            return _hypothesis_settings(**kwargs)(f)
        return wrapped

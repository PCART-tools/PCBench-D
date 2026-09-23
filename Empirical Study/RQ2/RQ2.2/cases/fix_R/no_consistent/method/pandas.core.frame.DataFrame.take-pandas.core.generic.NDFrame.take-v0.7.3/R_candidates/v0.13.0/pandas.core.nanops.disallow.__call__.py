    def __call__(self, f):
        @functools.wraps(f)
        def _f(*args, **kwargs):
            obj_iter = itertools.chain(args, compat.itervalues(kwargs))
            if any(self.check(obj) for obj in obj_iter):
                raise TypeError('reduction operation {0!r} not allowed for '
                                'this dtype'.format(f.__name__.replace('nan',
                                                                       '')))
            return f(*args, **kwargs)
        return _f

    def __call__(self, f):
        @functools.wraps(f)
        def _f(*args, **kwargs):
            obj_iter = itertools.chain(args, compat.itervalues(kwargs))
            if any(self.check(obj) for obj in obj_iter):
                msg = 'reduction operation {name!r} not allowed for this dtype'
                raise TypeError(msg.format(name=f.__name__.replace('nan', '')))
            try:
                with np.errstate(invalid='ignore'):
                    return f(*args, **kwargs)
            except ValueError as e:
                # we want to transform an object array
                # ValueError message to the more typical TypeError
                # e.g. this is normally a disallowed function on
                # object arrays that contain strings
                if is_object_dtype(args[0]):
                    raise TypeError(e)
                raise

        return _f

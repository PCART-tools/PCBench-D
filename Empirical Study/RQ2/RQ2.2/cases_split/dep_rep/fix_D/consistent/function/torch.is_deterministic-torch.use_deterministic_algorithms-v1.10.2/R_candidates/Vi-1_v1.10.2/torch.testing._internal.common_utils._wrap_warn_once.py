def _wrap_warn_once(regex):
    def decorator(fn):
        def inner(self, *args, **kwargs):
            with self.assertWarnsOnceRegex(UserWarning, regex):
                fn(self, *args, **kwargs)
        return inner
    return decorator

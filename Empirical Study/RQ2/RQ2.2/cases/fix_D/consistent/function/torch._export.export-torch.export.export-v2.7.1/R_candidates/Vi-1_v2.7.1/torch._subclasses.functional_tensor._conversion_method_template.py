def _conversion_method_template(**extra_kwargs):
    def _(self, *args, **kwargs):
        return self.to(*args, **{**kwargs, **extra_kwargs})

    return _

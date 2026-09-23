    def _reduce(self, name, axis=0, **kwargs):
        func = getattr(self, name, None)
        if func is None:
            msg = 'Categorical cannot perform the operation {op}'
            raise TypeError(msg.format(op=name))
        return func(**kwargs)

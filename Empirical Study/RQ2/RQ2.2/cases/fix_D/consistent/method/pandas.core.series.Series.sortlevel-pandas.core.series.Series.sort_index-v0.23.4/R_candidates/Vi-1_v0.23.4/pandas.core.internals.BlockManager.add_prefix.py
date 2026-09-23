    def add_prefix(self, prefix):
        f = partial('{prefix}{}'.format, prefix=prefix)
        return self.rename_axis(f, axis=0)

    def add_suffix(self, suffix):
        f = partial('{}{suffix}'.format, suffix=suffix)
        return self.rename_axis(f, axis=0)

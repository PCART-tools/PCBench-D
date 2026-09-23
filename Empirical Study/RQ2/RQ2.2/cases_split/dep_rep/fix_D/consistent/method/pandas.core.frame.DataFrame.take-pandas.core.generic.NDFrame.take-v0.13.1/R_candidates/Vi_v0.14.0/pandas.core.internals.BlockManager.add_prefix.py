    def add_prefix(self, prefix):
        f = (str(prefix) + '%s').__mod__
        return self.rename_axis(f, axis=0)

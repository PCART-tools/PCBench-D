    def add_prefix(self, prefix):
        f = (('%s' % prefix) + '%s').__mod__
        return self.rename_items(f)

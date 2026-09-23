    def __getitem__(self, name):
        self.ensure_not_dirty()
        if not self.avail:
            raise RuntimeError("No MovieWriters available!")
        try:
            return self.avail[name]
        except KeyError:
            raise RuntimeError(
                'Requested MovieWriter ({}) not available'.format(name))

    def __getitem__(self, name):
        self.ensure_not_dirty()
        if not self.avail:
            raise RuntimeError("No MovieWriters available!")
        return self.avail[name]

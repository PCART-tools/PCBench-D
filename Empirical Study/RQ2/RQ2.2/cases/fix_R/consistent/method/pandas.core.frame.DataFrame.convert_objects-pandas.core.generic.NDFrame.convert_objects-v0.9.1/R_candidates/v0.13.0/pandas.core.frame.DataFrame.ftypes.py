    @property
    def ftypes(self):
        return self.apply(lambda x: x.ftype, reduce=False)

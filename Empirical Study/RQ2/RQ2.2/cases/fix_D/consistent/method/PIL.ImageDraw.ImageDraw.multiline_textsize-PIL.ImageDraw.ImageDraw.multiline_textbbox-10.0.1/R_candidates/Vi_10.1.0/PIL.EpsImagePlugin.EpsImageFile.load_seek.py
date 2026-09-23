    def load_seek(self, *args, **kwargs):
        # we can't incrementally load, so force ImageFile.parser to
        # use our custom load method by defining this method.
        pass

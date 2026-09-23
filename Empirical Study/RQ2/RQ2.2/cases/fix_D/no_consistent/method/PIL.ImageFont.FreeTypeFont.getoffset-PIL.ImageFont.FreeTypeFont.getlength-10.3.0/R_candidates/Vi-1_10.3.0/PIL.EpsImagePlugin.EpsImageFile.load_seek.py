    def load_seek(self, pos):
        # we can't incrementally load, so force ImageFile.parser to
        # use our custom load method by defining this method.
        pass

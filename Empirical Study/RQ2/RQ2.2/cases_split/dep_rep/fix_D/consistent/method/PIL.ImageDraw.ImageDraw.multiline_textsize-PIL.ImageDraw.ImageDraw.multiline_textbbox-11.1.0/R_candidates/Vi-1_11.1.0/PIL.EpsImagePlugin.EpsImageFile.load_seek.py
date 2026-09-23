    def load_seek(self, pos: int) -> None:
        # we can't incrementally load, so force ImageFile.parser to
        # use our custom load method by defining this method.
        pass

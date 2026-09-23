    def __getattr__(self, elt):
        raise self.ex

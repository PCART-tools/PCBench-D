    def __iter__(self):
        proditer = product(*self.domains)
        return (sumsets(items) for items in proditer)

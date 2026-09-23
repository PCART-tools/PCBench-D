    def sem(self, ddof: int = 1, *args, **kwargs):
        return self.std(*args, **kwargs) / (self.count() - ddof).pow(0.5)

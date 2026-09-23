    @property
    def set(self):
        return ProductSet(domain.set for domain in self.domains)

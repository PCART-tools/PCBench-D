    def as_boolean(self):
        return And(*[domain.as_boolean() for domain in self.domains])

    def __call__(self, factory):
        register_payload(factory, self.type)
        return factory

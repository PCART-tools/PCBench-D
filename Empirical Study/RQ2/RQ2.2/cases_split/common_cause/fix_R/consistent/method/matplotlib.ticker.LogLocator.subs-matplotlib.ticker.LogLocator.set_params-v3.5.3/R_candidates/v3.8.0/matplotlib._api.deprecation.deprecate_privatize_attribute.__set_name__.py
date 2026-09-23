    def __set_name__(self, owner, name):
        setattr(owner, name, self.deprecator(
            property(lambda self: getattr(self, f"_{name}"),
                     lambda self, value: setattr(self, f"_{name}", value)),
            name=name))

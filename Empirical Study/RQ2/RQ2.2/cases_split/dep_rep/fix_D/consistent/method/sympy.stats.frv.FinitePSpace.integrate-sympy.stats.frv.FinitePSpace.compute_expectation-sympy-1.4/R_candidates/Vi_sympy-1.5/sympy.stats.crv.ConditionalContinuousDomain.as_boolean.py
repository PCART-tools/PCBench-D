    def as_boolean(self):
        return And(self.fulldomain.as_boolean(), self.condition)

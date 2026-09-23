    def is_type_compatible(self, typ):
        return typ == self.inferred_type or typ == "timedelta"

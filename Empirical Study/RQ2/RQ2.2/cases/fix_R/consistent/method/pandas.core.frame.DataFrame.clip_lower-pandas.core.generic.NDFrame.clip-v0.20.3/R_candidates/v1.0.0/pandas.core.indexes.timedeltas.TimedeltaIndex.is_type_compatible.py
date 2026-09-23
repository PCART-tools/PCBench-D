    def is_type_compatible(self, typ) -> bool:
        return typ == self.inferred_type or typ == "timedelta"

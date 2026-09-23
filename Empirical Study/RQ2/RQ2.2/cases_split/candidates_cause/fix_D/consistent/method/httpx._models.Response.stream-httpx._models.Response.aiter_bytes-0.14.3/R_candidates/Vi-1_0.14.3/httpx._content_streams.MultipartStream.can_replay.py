    def can_replay(self) -> bool:
        return all(field.can_replay() for field in self.fields)

    def __contains__(self, key: int) -> bool:
        return key in self.existing_entries or key in self.new_entries

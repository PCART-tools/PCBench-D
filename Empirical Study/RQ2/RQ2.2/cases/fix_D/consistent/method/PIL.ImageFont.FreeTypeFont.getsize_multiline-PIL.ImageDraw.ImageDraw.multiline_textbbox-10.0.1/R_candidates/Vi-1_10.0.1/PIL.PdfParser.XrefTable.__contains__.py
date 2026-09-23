    def __contains__(self, key):
        return key in self.existing_entries or key in self.new_entries

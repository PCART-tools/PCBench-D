    def keys(self) -> set[int]:
        return (
            set(self.existing_entries.keys()) - set(self.deleted_entries.keys())
        ) | set(self.new_entries.keys())

    def __len__(self):
        return len(
            set(self.existing_entries.keys())
            | set(self.new_entries.keys())
            | set(self.deleted_entries.keys())
        )

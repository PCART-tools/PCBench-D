    def __getitem__(self, key: int) -> tuple[int, int]:
        try:
            return self.new_entries[key]
        except KeyError:
            return self.existing_entries[key]

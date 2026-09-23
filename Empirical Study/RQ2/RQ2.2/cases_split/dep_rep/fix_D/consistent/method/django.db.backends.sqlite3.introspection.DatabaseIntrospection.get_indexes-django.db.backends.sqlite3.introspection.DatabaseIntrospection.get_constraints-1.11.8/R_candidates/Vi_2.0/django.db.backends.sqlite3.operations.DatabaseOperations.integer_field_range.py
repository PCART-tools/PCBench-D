    def integer_field_range(self, internal_type):
        # SQLite doesn't enforce any integer constraints
        return (None, None)

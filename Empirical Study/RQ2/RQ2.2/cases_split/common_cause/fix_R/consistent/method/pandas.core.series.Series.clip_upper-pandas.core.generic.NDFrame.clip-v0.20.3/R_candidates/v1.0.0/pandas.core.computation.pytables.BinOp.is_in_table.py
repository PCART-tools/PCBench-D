    @property
    def is_in_table(self) -> bool:
        """ return True if this is a valid column name for generation (e.g. an
        actual column in the table) """
        return self.queryables.get(self.lhs) is not None

    def _name_to_index(self, cursor, table_name):
        """
        Returns a dictionary of {field_name: field_index} for the given table.
        Indexes are 0-based.
        """
        return {d[0]: i for i, d in enumerate(self.get_table_description(cursor, table_name))}

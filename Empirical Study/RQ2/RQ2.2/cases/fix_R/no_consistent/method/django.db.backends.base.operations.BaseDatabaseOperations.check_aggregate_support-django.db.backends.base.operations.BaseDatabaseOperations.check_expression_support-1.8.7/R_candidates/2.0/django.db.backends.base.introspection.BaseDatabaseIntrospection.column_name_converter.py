    def column_name_converter(self, name):
        """
        Apply a conversion to the column name for the purposes of comparison.

        Use table_name_converter() by default.
        """
        return self.table_name_converter(name)

    def get_table_description(self, cursor, table_name):
        """
        Return a description of the table with the DB-API cursor.description
        interface.
        """
        return [
            FieldInfo(
                info['name'],
                info['type'],
                None,
                info['size'],
                None,
                None,
                info['null_ok'],
                info['default'],
            ) for info in self._table_info(cursor, table_name)
        ]

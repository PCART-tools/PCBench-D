    def get_table_list(self, cursor):
        """Return a list of table and view names in the current database."""
        cursor.execute("SELECT TABLE_NAME, 't' FROM USER_TABLES UNION ALL "
                       "SELECT VIEW_NAME, 'v' FROM USER_VIEWS")
        return [TableInfo(row[0].lower(), row[1]) for row in cursor.fetchall()]

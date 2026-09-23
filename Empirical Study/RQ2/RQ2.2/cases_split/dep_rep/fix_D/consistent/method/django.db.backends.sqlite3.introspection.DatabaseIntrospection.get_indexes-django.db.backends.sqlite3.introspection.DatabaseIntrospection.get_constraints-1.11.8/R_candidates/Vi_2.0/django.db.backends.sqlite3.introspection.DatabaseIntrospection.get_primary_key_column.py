    def get_primary_key_column(self, cursor, table_name):
        """Return the column name of the primary key for the given table."""
        # Don't use PRAGMA because that causes issues with some transactions
        cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s", [table_name, "table"])
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Table %s does not exist" % table_name)
        results = row[0].strip()
        results = results[results.index('(') + 1:results.rindex(')')]
        for field_desc in results.split(','):
            field_desc = field_desc.strip()
            m = re.search('"(.*)".*PRIMARY KEY( AUTOINCREMENT)?', field_desc)
            if m:
                return m.groups()[0]
        return None

    def get_key_columns(self, cursor, table_name):
        """
        Return a list of (column_name, referenced_table_name, referenced_column_name)
        for all key columns in given table.
        """
        key_columns = []

        # Schema for this table
        cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s", [table_name, "table"])
        results = cursor.fetchone()[0].strip()
        results = results[results.index('(') + 1:results.rindex(')')]

        # Walk through and look for references to other tables. SQLite doesn't
        # really have enforced references, but since it echoes out the SQL used
        # to create the table we can look for REFERENCES statements used there.
        for field_index, field_desc in enumerate(results.split(',')):
            field_desc = field_desc.strip()
            if field_desc.startswith("UNIQUE"):
                continue

            m = re.search(r'"(.*)".*references (.*) \(["|](.*)["|]\)', field_desc, re.I)
            if not m:
                continue

            # This will append (column_name, referenced_table_name, referenced_column_name) to key_columns
            key_columns.append(tuple(s.strip('"') for s in m.groups()))

        return key_columns

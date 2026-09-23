    def get_relations(self, cursor, table_name):
        """
        Return a dictionary of {field_name: (field_name_other_table, other_table)}
        representing all relationships to the given table.
        """
        # Dictionary of relations to return
        relations = {}

        # Schema for this table
        cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s", [table_name, "table"])
        try:
            results = cursor.fetchone()[0].strip()
        except TypeError:
            # It might be a view, then no results will be returned
            return relations
        results = results[results.index('(') + 1:results.rindex(')')]

        # Walk through and look for references to other tables. SQLite doesn't
        # really have enforced references, but since it echoes out the SQL used
        # to create the table we can look for REFERENCES statements used there.
        for field_desc in results.split(','):
            field_desc = field_desc.strip()
            if field_desc.startswith("UNIQUE"):
                continue

            m = re.search(r'references (\S*) ?\(["|]?(.*)["|]?\)', field_desc, re.I)
            if not m:
                continue
            table, column = [s.strip('"') for s in m.groups()]

            if field_desc.startswith("FOREIGN KEY"):
                # Find name of the target FK field
                m = re.match(r'FOREIGN KEY\s*\(([^\)]*)\).*', field_desc, re.I)
                field_name = m.groups()[0].strip('"')
            else:
                field_name = field_desc.split()[0].strip('"')

            cursor.execute("SELECT sql FROM sqlite_master WHERE tbl_name = %s", [table])
            result = cursor.fetchall()[0]
            other_table_results = result[0].strip()
            li, ri = other_table_results.index('('), other_table_results.rindex(')')
            other_table_results = other_table_results[li + 1:ri]

            for other_desc in other_table_results.split(','):
                other_desc = other_desc.strip()
                if other_desc.startswith('UNIQUE'):
                    continue

                other_name = other_desc.split(' ', 1)[0].strip('"')
                if other_name == column:
                    relations[field_name] = (other_name, table)
                    break

        return relations

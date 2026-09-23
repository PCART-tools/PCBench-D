    def get_relations(self, cursor, table_name):
        """
        Return a dictionary of {field_name: (field_name_other_table, other_table)}
        representing all relationships to the given table.
        """
        table_name = table_name.upper()
        cursor.execute("""
    SELECT ca.column_name, cb.table_name, cb.column_name
    FROM   user_constraints, USER_CONS_COLUMNS ca, USER_CONS_COLUMNS cb
    WHERE  user_constraints.table_name = %s AND
           user_constraints.constraint_name = ca.constraint_name AND
           user_constraints.r_constraint_name = cb.constraint_name AND
           ca.position = cb.position""", [table_name])

        relations = {}
        for row in cursor.fetchall():
            relations[row[0].lower()] = (row[2].lower(), row[1].lower())
        return relations

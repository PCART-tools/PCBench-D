    def get_relations(self, cursor, table_name):
        """
        Returns a dictionary of {field_name: (field_name_other_table, other_table)}
        representing all relationships to the given table.
        """
        table_name = table_name.upper()
        cursor.execute("""
    SELECT ta.column_name, tb.table_name, tb.column_name
    FROM   user_constraints, USER_CONS_COLUMNS ca, USER_CONS_COLUMNS cb,
           user_tab_cols ta, user_tab_cols tb
    WHERE  user_constraints.table_name = %s AND
           ta.table_name = user_constraints.table_name AND
           ta.column_name = ca.column_name AND
           ca.table_name = ta.table_name AND
           user_constraints.constraint_name = ca.constraint_name AND
           user_constraints.r_constraint_name = cb.constraint_name AND
           cb.table_name = tb.table_name AND
           cb.column_name = tb.column_name AND
           ca.position = cb.position""", [table_name])

        relations = {}
        for row in cursor.fetchall():
            relations[row[0].lower()] = (row[2].lower(), row[1].lower())
        return relations

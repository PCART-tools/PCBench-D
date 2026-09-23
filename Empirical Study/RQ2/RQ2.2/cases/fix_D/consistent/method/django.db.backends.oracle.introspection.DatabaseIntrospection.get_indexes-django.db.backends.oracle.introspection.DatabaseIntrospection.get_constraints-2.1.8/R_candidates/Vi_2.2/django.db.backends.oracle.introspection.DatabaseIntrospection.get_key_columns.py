    def get_key_columns(self, cursor, table_name):
        cursor.execute("""
            SELECT ccol.column_name, rcol.table_name AS referenced_table, rcol.column_name AS referenced_column
            FROM user_constraints c
            JOIN user_cons_columns ccol
              ON ccol.constraint_name = c.constraint_name
            JOIN user_cons_columns rcol
              ON rcol.constraint_name = c.r_constraint_name
            WHERE c.table_name = %s AND c.constraint_type = 'R'""", [table_name.upper()])
        return [
            tuple(self.identifier_converter(cell) for cell in row)
            for row in cursor.fetchall()
        ]

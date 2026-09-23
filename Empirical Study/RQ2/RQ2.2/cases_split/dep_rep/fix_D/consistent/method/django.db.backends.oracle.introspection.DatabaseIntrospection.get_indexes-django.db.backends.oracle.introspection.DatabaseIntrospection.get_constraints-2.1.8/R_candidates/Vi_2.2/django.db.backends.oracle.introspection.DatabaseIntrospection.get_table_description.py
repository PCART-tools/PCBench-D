    def get_table_description(self, cursor, table_name):
        """
        Return a description of the table with the DB-API cursor.description
        interface.
        """
        # user_tab_columns gives data default for columns
        cursor.execute("""
            SELECT
                column_name,
                data_default,
                CASE
                    WHEN char_used IS NULL THEN data_length
                    ELSE char_length
                END as internal_size,
                CASE
                    WHEN identity_column = 'YES' THEN 1
                    ELSE 0
                END as is_autofield
            FROM user_tab_cols
            WHERE table_name = UPPER(%s)""", [table_name])
        field_map = {
            column: (internal_size, default if default != 'NULL' else None, is_autofield)
            for column, default, internal_size, is_autofield in cursor.fetchall()
        }
        self.cache_bust_counter += 1
        cursor.execute("SELECT * FROM {} WHERE ROWNUM < 2 AND {} > 0".format(
            self.connection.ops.quote_name(table_name),
            self.cache_bust_counter))
        description = []
        for desc in cursor.description:
            name = desc[0]
            internal_size, default, is_autofield = field_map[name]
            name = name % {}  # cx_Oracle, for some reason, doubles percent signs.
            description.append(FieldInfo(
                self.identifier_converter(name), *desc[1:3], internal_size, desc[4] or 0,
                desc[5] or 0, *desc[6:], default, is_autofield,
            ))
        return description

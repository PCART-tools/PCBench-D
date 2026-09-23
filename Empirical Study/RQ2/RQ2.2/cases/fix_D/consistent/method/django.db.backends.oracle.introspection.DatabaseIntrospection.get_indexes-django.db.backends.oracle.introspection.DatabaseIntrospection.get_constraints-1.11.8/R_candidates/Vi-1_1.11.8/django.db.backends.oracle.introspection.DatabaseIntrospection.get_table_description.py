    def get_table_description(self, cursor, table_name):
        "Returns a description of the table, with the DB-API cursor.description interface."
        # user_tab_columns gives data default for columns
        cursor.execute("""
            SELECT
                column_name,
                data_default,
                CASE
                    WHEN char_used IS NULL THEN data_length
                    ELSE char_length
                END as internal_size
            FROM user_tab_cols
            WHERE table_name = UPPER(%s)""", [table_name])
        field_map = {
            column: (internal_size, default if default != 'NULL' else None)
            for column, default, internal_size in cursor.fetchall()
        }
        self.cache_bust_counter += 1
        cursor.execute("SELECT * FROM {} WHERE ROWNUM < 2 AND {} > 0".format(
            self.connection.ops.quote_name(table_name),
            self.cache_bust_counter))
        description = []
        for desc in cursor.description:
            name = force_text(desc[0])  # cx_Oracle always returns a 'str' on both Python 2 and 3
            internal_size, default = field_map[name]
            name = name % {}  # cx_Oracle, for some reason, doubles percent signs.
            description.append(FieldInfo(*(
                (name.lower(),) +
                desc[1:3] +
                (internal_size, desc[4] or 0, desc[5] or 0) +
                desc[6:] +
                (default,)
            )))
        return description

    def get_table_list(self, cursor):
        """Return a list of table and view names in the current database."""
        cursor.execute("""
            SELECT table_name, 't'
            FROM user_tables
            WHERE
                NOT EXISTS (
                    SELECT 1
                    FROM user_mviews
                    WHERE user_mviews.mview_name = user_tables.table_name
                )
            UNION ALL
            SELECT view_name, 'v' FROM user_views
            UNION ALL
            SELECT mview_name, 'v' FROM user_mviews
        """)
        return [TableInfo(self.identifier_converter(row[0]), row[1]) for row in cursor.fetchall()]

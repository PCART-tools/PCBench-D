    def get_indexes(self, cursor, table_name):
        warnings.warn(
            "get_indexes() is deprecated in favor of get_constraints().",
            RemovedInDjango21Warning, stacklevel=2
        )
        sql = """
    SELECT LOWER(uic1.column_name) AS column_name,
           CASE user_constraints.constraint_type
               WHEN 'P' THEN 1 ELSE 0
           END AS is_primary_key,
           CASE user_indexes.uniqueness
               WHEN 'UNIQUE' THEN 1 ELSE 0
           END AS is_unique
    FROM   user_constraints, user_indexes, user_ind_columns uic1
    WHERE  user_constraints.constraint_type (+) = 'P'
      AND  user_constraints.index_name (+) = uic1.index_name
      AND  user_indexes.uniqueness (+) = 'UNIQUE'
      AND  user_indexes.index_name (+) = uic1.index_name
      AND  uic1.table_name = UPPER(%s)
      AND  uic1.column_position = 1
      AND  NOT EXISTS (
              SELECT 1
              FROM   user_ind_columns uic2
              WHERE  uic2.index_name = uic1.index_name
                AND  uic2.column_position = 2
           )
        """
        cursor.execute(sql, [table_name])
        indexes = {}
        for row in cursor.fetchall():
            indexes[row[0]] = {'primary_key': bool(row[1]),
                               'unique': bool(row[2])}
        return indexes

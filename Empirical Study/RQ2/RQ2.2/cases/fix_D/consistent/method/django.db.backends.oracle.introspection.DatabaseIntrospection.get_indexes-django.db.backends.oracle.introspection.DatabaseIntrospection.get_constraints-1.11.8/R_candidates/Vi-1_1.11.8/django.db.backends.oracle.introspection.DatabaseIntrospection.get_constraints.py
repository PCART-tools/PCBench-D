    def get_constraints(self, cursor, table_name):
        """
        Retrieves any constraints or keys (unique, pk, fk, check, index) across one or more columns.
        """
        constraints = {}
        # Loop over the constraints, getting PKs, uniques, and checks
        cursor.execute("""
            SELECT
                user_constraints.constraint_name,
                LOWER(cols.column_name) AS column_name,
                CASE user_constraints.constraint_type
                    WHEN 'P' THEN 1
                    ELSE 0
                END AS is_primary_key,
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM user_indexes
                        WHERE user_indexes.index_name = user_constraints.index_name
                        AND user_indexes.uniqueness = 'UNIQUE'
                    )
                    THEN 1
                    ELSE 0
                END AS is_unique,
                CASE user_constraints.constraint_type
                    WHEN 'C' THEN 1
                    ELSE 0
                END AS is_check_constraint,
                CASE
                    WHEN user_constraints.constraint_type IN ('P', 'U') THEN 1
                    ELSE 0
                END AS has_index
            FROM
                user_constraints
            LEFT OUTER JOIN
                user_cons_columns cols ON user_constraints.constraint_name = cols.constraint_name
            WHERE
                user_constraints.constraint_type = ANY('P', 'U', 'C')
                AND user_constraints.table_name = UPPER(%s)
            ORDER BY cols.position
        """, [table_name])
        for constraint, column, pk, unique, check, index in cursor.fetchall():
            # If we're the first column, make the record
            if constraint not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "primary_key": pk,
                    "unique": unique,
                    "foreign_key": None,
                    "check": check,
                    "index": index,  # All P and U come with index
                }
            # Record the details
            constraints[constraint]['columns'].append(column)
        # Foreign key constraints
        cursor.execute("""
            SELECT
                cons.constraint_name,
                LOWER(cols.column_name) AS column_name,
                LOWER(rcols.table_name),
                LOWER(rcols.column_name)
            FROM
                user_constraints cons
            INNER JOIN
                user_cons_columns rcols ON rcols.constraint_name = cons.r_constraint_name
            LEFT OUTER JOIN
                user_cons_columns cols ON cons.constraint_name = cols.constraint_name
            WHERE
                cons.constraint_type = 'R' AND
                cons.table_name = UPPER(%s)
            ORDER BY cols.position
        """, [table_name])
        for constraint, column, other_table, other_column in cursor.fetchall():
            # If we're the first column, make the record
            if constraint not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "primary_key": False,
                    "unique": False,
                    "foreign_key": (other_table, other_column),
                    "check": False,
                    "index": False,
                }
            # Record the details
            constraints[constraint]['columns'].append(column)
        # Now get indexes
        cursor.execute("""
            SELECT
                cols.index_name, LOWER(cols.column_name), cols.descend,
                LOWER(ind.index_type)
            FROM
                user_ind_columns cols, user_indexes ind
            WHERE
                cols.table_name = UPPER(%s) AND
                NOT EXISTS (
                    SELECT 1
                    FROM user_constraints cons
                    WHERE cols.index_name = cons.index_name
                ) AND cols.index_name = ind.index_name
            ORDER BY cols.column_position
        """, [table_name])
        for constraint, column, order, type_ in cursor.fetchall():
            # If we're the first column, make the record
            if constraint not in constraints:
                constraints[constraint] = {
                    "columns": [],
                    "orders": [],
                    "primary_key": False,
                    "unique": False,
                    "foreign_key": None,
                    "check": False,
                    "index": True,
                    "type": 'idx' if type_ == 'normal' else type_,
                }
            # Record the details
            constraints[constraint]['columns'].append(column)
            constraints[constraint]['orders'].append(order)
        return constraints

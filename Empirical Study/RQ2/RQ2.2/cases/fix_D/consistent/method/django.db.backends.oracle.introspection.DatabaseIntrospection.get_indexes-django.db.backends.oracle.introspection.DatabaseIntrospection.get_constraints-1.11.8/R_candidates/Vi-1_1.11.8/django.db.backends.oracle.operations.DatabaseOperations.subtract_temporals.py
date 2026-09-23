    def subtract_temporals(self, internal_type, lhs, rhs):
        if internal_type == 'DateField':
            lhs_sql, lhs_params = lhs
            rhs_sql, rhs_params = rhs
            return "NUMTODSINTERVAL(%s - %s, 'DAY')" % (lhs_sql, rhs_sql), lhs_params + rhs_params
        return super(DatabaseOperations, self).subtract_temporals(internal_type, lhs, rhs)

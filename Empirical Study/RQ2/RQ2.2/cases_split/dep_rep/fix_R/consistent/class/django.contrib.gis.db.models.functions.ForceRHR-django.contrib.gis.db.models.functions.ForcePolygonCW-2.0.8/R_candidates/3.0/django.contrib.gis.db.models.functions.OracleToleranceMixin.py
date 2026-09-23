class OracleToleranceMixin:
    tolerance = 0.05

    def as_oracle(self, compiler, connection, **extra_context):
        tol = self.extra.get('tolerance', self.tolerance)
        return self.as_sql(
            compiler, connection,
            template="%%(function)s(%%(expressions)s, %s)" % tol,
            **extra_context
        )

    def combine_expression(self, connector, sub_expressions):
        # SQLite doesn't have a power function, so we fake it with a
        # user-defined function django_power that's registered in connect().
        if connector == '^':
            return 'django_power(%s)' % ','.join(sub_expressions)
        return super().combine_expression(connector, sub_expressions)

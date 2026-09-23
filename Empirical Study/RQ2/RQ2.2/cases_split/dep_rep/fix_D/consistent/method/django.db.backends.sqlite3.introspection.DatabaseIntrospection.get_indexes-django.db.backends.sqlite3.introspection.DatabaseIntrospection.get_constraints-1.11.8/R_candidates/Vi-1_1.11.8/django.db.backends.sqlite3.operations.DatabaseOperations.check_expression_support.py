    def check_expression_support(self, expression):
        bad_fields = (fields.DateField, fields.DateTimeField, fields.TimeField)
        bad_aggregates = (aggregates.Sum, aggregates.Avg, aggregates.Variance, aggregates.StdDev)
        if isinstance(expression, bad_aggregates):
            for expr in expression.get_source_expressions():
                try:
                    output_field = expr.output_field
                    if isinstance(output_field, bad_fields):
                        raise NotImplementedError(
                            'You cannot use Sum, Avg, StdDev, and Variance '
                            'aggregations on date/time fields in sqlite3 '
                            'since date/time is saved as text.'
                        )
                except FieldError:
                    # Not every subexpression has an output_field which is fine
                    # to ignore.
                    pass

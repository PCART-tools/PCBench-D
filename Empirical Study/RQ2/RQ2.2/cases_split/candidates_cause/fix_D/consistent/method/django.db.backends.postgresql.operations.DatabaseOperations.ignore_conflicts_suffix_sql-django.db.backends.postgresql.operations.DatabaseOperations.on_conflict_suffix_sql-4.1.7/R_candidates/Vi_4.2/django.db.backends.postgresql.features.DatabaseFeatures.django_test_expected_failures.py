    @cached_property
    def django_test_expected_failures(self):
        expected_failures = set()
        if self.uses_server_side_binding:
            expected_failures.update(
                {
                    # Parameters passed to expressions in SELECT and GROUP BY
                    # clauses are not recognized as the same values when using
                    # server-side binding cursors (#34255).
                    "aggregation.tests.AggregateTestCase."
                    "test_group_by_nested_expression_with_params",
                }
            )
        return expected_failures

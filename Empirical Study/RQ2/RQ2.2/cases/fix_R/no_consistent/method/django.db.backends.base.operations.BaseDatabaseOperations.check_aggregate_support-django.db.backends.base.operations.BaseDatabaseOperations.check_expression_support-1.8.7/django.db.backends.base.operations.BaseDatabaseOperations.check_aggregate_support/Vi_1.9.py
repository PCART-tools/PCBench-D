    def check_aggregate_support(self, aggregate_func):
        warnings.warn(
            "check_aggregate_support has been deprecated. Use "
            "check_expression_support instead.",
            RemovedInDjango20Warning, stacklevel=2)
        return self.check_expression_support(aggregate_func)

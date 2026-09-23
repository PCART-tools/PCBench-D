    @staticmethod
    @cache
    def number_of_parameters(func):
        """Return number of parameters of the callable *func*."""
        return len(inspect.signature(func).parameters)

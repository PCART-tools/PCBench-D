    def _get_methods(cls):
        import inspect

        # In Python 3 unbound methods are functions, but in Python 2 they are methods
        return inspect.getmembers(
            cls, predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x)
        )

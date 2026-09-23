    def agg(self):
        result = super().agg()
        if result is None:
            obj = self.obj
            func = self.func
            # string, list-like, and dict-like are entirely handled in super
            assert callable(func)

            # GH53325: The setup below is just to keep current behavior while emitting a
            # deprecation message. In the future this will all be replaced with a simple
            # `result = f(self.obj, *self.args, **self.kwargs)`.
            try:
                result = obj.apply(func, args=self.args, **self.kwargs)
            except (ValueError, AttributeError, TypeError):
                result = func(obj, *self.args, **self.kwargs)
            else:
                msg = (
                    f"using {func} in {type(obj).__name__}.agg cannot aggregate and "
                    f"has been deprecated. Use {type(obj).__name__}.transform to "
                    f"keep behavior unchanged."
                )
                warnings.warn(msg, FutureWarning, stacklevel=find_stack_level())

        return result

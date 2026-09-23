    def agg(self):
        result = super().agg()
        if result is None:
            f = self.f
            kwargs = self.kwargs

            # string, list-like, and dict-like are entirely handled in super
            assert callable(f)

            # we can be called from an inner function which
            # passes this meta-data
            kwargs.pop("_level", None)

            # try a regular apply, this evaluates lambdas
            # row-by-row; however if the lambda is expected a Series
            # expression, e.g.: lambda x: x-x.quantile(0.25)
            # this will fail, so we can try a vectorized evaluation

            # we cannot FIRST try the vectorized evaluation, because
            # then .agg and .apply would have different semantics if the
            # operation is actually defined on the Series, e.g. str
            try:
                result = self.obj.apply(f)
            except (ValueError, AttributeError, TypeError):
                result = f(self.obj)

        return result

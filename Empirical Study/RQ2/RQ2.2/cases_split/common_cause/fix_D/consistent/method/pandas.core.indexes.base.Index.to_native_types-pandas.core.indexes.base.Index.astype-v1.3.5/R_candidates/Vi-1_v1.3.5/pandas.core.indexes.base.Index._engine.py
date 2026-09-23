    @cache_readonly
    def _engine(self) -> libindex.IndexEngine:
        # For base class (object dtype) we get ObjectEngine

        # to avoid a reference cycle, bind `target_values` to a local variable, so
        # `self` is not passed into the lambda.
        target_values = self._get_engine_target()
        return self._engine_type(lambda: target_values, len(self))

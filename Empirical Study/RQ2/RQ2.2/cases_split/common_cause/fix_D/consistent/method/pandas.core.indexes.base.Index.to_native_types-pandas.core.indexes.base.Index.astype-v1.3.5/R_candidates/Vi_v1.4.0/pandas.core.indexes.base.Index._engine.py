    @cache_readonly
    def _engine(
        self,
    ) -> libindex.IndexEngine:
        # For base class (object dtype) we get ObjectEngine

        if isinstance(self._values, BaseMaskedArray):
            # TODO(ExtensionIndex): use libindex.NullableEngine(self._values)
            return libindex.ObjectEngine(self._get_engine_target())
        elif (
            isinstance(self._values, ExtensionArray)
            and self._engine_type is libindex.ObjectEngine
        ):
            # TODO(ExtensionIndex): use libindex.ExtensionEngine(self._values)
            return libindex.ObjectEngine(self._get_engine_target())

        # to avoid a reference cycle, bind `target_values` to a local variable, so
        # `self` is not passed into the lambda.
        target_values = self._get_engine_target()
        return self._engine_type(target_values)

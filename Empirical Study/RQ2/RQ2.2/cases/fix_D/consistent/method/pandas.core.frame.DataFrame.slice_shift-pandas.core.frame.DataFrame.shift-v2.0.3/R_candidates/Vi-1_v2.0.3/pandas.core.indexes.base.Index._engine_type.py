    @property
    def _engine_type(
        self,
    ) -> type[libindex.IndexEngine] | type[libindex.ExtensionEngine]:
        return self._engine_types.get(self.dtype, libindex.ObjectEngine)

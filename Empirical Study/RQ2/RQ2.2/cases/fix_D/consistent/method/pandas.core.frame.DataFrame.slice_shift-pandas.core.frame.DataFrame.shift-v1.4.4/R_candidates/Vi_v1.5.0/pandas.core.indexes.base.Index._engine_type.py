    @property
    def _engine_type(
        self,
    ) -> type[libindex.IndexEngine] | type[libindex.ExtensionEngine]:
        return libindex.ObjectEngine

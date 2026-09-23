    def _is_memory_usage_qualified(self):
        """ return a boolean if we need a qualified .info display """

        def f(l):
            return "mixed" in l or "string" in l or "unicode" in l

        return any(f(l) for l in self._inferred_type_levels)

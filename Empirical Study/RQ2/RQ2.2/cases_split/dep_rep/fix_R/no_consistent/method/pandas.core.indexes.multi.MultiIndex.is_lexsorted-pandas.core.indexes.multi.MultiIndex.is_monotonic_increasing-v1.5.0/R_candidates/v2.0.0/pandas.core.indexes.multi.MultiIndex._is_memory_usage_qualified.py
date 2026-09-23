    def _is_memory_usage_qualified(self) -> bool:
        """return a boolean if we need a qualified .info display"""

        def f(level) -> bool:
            return "mixed" in level or "string" in level or "unicode" in level

        return any(f(level) for level in self._inferred_type_levels)

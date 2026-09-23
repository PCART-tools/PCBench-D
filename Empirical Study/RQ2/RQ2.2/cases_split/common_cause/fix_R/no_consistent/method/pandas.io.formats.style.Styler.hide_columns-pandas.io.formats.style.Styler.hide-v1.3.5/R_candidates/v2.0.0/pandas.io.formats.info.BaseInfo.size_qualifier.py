    @property
    def size_qualifier(self) -> str:
        size_qualifier = ""
        if self.memory_usage:
            if self.memory_usage != "deep":
                # size_qualifier is just a best effort; not guaranteed to catch
                # all cases (e.g., it misses categorical data even with object
                # categories)
                if (
                    "object" in self.dtype_counts
                    or self.data.index._is_memory_usage_qualified()
                ):
                    size_qualifier = "+"
        return size_qualifier

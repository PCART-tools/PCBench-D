    @property
    def display_memory_usage(self) -> bool:
        """Whether to display memory usage."""
        return bool(self.info.memory_usage)

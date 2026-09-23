    def add_memory_usage_line(self) -> None:
        """Add line containing memory usage."""
        self._lines.append(f"memory usage: {self.memory_usage_string}")

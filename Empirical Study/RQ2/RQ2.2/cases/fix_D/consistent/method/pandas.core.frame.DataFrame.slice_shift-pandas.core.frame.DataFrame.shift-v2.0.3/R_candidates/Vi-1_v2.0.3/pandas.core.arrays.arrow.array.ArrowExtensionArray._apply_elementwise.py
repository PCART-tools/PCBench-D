    def _apply_elementwise(self, func: Callable) -> list[list[Any]]:
        """Apply a callable to each element while maintaining the chunking structure."""
        return [
            [
                None if val is None else func(val)
                for val in chunk.to_numpy(zero_copy_only=False)
            ]
            for chunk in self._data.iterchunks()
        ]

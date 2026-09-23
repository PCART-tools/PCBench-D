    @property
    def _is_aligned(self) -> bool:
        return self.aligned_axes is not None and self.result_type is not None

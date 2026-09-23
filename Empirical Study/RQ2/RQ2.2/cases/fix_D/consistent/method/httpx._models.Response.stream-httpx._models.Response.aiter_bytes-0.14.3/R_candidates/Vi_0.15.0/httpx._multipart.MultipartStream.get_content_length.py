    def get_content_length(self) -> int:
        return sum(self.iter_chunks_lengths())

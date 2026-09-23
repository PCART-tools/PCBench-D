    def check_text_memory(self, chunklen):
        self.text_memory += chunklen
        if self.text_memory > MAX_TEXT_MEMORY:
            msg = (
                "Too much memory used in text chunks: "
                f"{self.text_memory}>MAX_TEXT_MEMORY"
            )
            raise ValueError(msg)
